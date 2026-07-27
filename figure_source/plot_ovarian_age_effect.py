#!/usr/bin/env python3
"""Draw the single-column ovarian age-associated transfer case study."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA_PATH = HERE / "ovarian_age_effect_values.csv"
OUTPUT_STEM = ROOT / "ovarian_age_effect_single_column"

MATCHED_COLOR = "#2166AC"
SHIFTED_COLOR = "#D6604D"
GRID_COLOR = "#D9DDE3"
TEXT_COLOR = "#222222"

PANEL_ORDER = [
    "Predictive performance",
    "Prediction sparsity",
    "Distribution distance",
]
PANEL_TITLES = {
    "Predictive performance": "Predictive performance",
    "Prediction sparsity": "Prediction sparsity",
    "Distribution distance": "Distribution distance",
}
PANEL_NOTES = {
    "Predictive performance": "higher is better",
    "Prediction sparsity": "diagnostic statistics",
    "Distribution distance": "lower is closer",
}
PANEL_LIMITS = {
    "Predictive performance": (0.0, 0.335),
    "Prediction sparsity": (0.0, 0.190),
    "Distribution distance": (0.0, 1.190),
}


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.2,
            "axes.titlesize": 8.1,
            "axes.labelsize": 7.2,
            "xtick.labelsize": 6.8,
            "ytick.labelsize": 6.7,
            "legend.fontsize": 6.8,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def add_value_labels(ax: plt.Axes, bars, upper: float) -> None:
    offset = upper * 0.018
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + offset,
            f"{height:.3f}",
            ha="center",
            va="bottom",
            fontsize=6.3,
            color=TEXT_COLOR,
        )


def draw_panel(
    ax: plt.Axes,
    panel_data: pd.DataFrame,
    panel_name: str,
    panel_letter: str,
) -> None:
    x = np.arange(len(panel_data))
    width = 0.34
    matched = ax.bar(
        x - width / 2,
        panel_data["matched_older_band"],
        width,
        color=MATCHED_COLOR,
        edgecolor="white",
        linewidth=0.45,
        label=r"Matched: 60+ $\rightarrow$ 60+",
        zorder=3,
    )
    shifted = ax.bar(
        x + width / 2,
        panel_data["age_shifted_band"],
        width,
        color=SHIFTED_COLOR,
        edgecolor="white",
        linewidth=0.45,
        label=r"Age-shifted: 60+ $\rightarrow$ <40",
        zorder=3,
    )

    lower, upper = PANEL_LIMITS[panel_name]
    ax.set_ylim(lower, upper)
    ax.set_xticks(x)
    ax.set_xticklabels(panel_data["metric"])
    ax.set_ylabel("Metric value")
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.55, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#6B7280")
    ax.spines["bottom"].set_color("#6B7280")
    ax.tick_params(colors="#4B5563")

    ax.text(
        0.0,
        1.055,
        panel_letter,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.7,
        fontweight="bold",
        color=TEXT_COLOR,
    )
    ax.text(
        0.075,
        1.055,
        PANEL_TITLES[panel_name],
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.1,
        fontweight="bold",
        color=TEXT_COLOR,
    )
    ax.text(
        1.0,
        1.055,
        PANEL_NOTES[panel_name],
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.3,
        color="#5E6673",
    )

    add_value_labels(ax, matched, upper)
    add_value_labels(ax, shifted, upper)


def main() -> None:
    configure_style()
    data = pd.read_csv(DATA_PATH)

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(3.48, 5.45),
        constrained_layout=False,
        gridspec_kw={"hspace": 0.56},
    )

    for letter, panel_name, ax in zip("abc", PANEL_ORDER, axes):
        panel_data = data.loc[data["panel"] == panel_name].reset_index(drop=True)
        draw_panel(ax, panel_data, panel_name, letter)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.995),
        frameon=False,
        ncol=1,
        handlelength=1.4,
        handletextpad=0.55,
        labelspacing=0.25,
    )
    fig.subplots_adjust(left=0.16, right=0.985, top=0.895, bottom=0.075)

    pdf_metadata = {
        "Title": "Ovarian age-associated transfer case study",
        "Subject": "Single-column redraw from reported benchmark values",
    }
    svg_metadata = {
        "Title": "Ovarian age-associated transfer case study",
        "Description": "Single-column redraw from reported benchmark values",
    }
    fig.savefig(
        OUTPUT_STEM.with_suffix(".pdf"),
        bbox_inches="tight",
        pad_inches=0.02,
        metadata=pdf_metadata,
    )
    fig.savefig(
        OUTPUT_STEM.with_suffix(".svg"),
        bbox_inches="tight",
        pad_inches=0.02,
        metadata=svg_metadata,
    )
    fig.savefig(
        OUTPUT_STEM.with_suffix(".png"),
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.02,
        facecolor="white",
    )
    fig.savefig(
        OUTPUT_STEM.with_suffix(".tiff"),
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.02,
        facecolor="white",
        pil_kwargs={"compression": "tiff_lzw"},
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
