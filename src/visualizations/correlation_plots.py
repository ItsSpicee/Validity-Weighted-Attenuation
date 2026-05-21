"""
src/visualizations/correlation_plots.py
----------------------------------------
Correlation change visualizations before and after attenuation.

Produces:
  1. Pearson and Spearman correlation bar charts (before vs after attenuation)
  2. Weighted average % change in correlation magnitude per topic
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, spearmanr
from catboost import CatBoostRegressor

from constants import (
    ATTUNED_RATINGS,
    FINAL_EMOTIONS,
    METADATA_COLS,
    MISC_D_COL,
    POS_EMOTIONS,
    NEG_EMOTIONS,
    TOPICS,             
    TOPIC_DISPLAY_NAMES,
    
)

POLARITIES  = ["pos", "neg"]



# ==============================================================================
# HELPERS
# ==============================================================================

def _get_emotion_columns(df: pd.DataFrame, topic: str, polarity: str) -> list[str]:
    base = POS_EMOTIONS if polarity == "pos" else NEG_EMOTIONS
    return [f"{e}_{topic}" for e in base if f"{e}_{topic}" in df.columns]


def _compute_corr(x: pd.Series, y: pd.Series) -> tuple[float, float, float, float]:
    p, p_val = pearsonr(x, y)
    s, s_val = spearmanr(x, y)
    return p, p_val, s, s_val


def _print_corr(p, p_val, s, s_val, label: str) -> None:
    print(
        f"  {label}:\n"
        f"    Pearson: {p:.4f} (p={p_val:.4f}) | "
        f"Spearman: {s:.4f} (p={s_val:.4f})"
    )



# ==============================================================================
# CORRELATION RECORDS
# ==============================================================================

def build_corr_records(
    df_data: pd.DataFrame,
    final_df: pd.DataFrame,
) -> pd.DataFrame:
    """Compute raw and attuned correlations for every topic/polarity combination."""
    corr_records = []
    att_rating = final_df["rating"] + final_df["weighting_delta"]

    #iterates over the topic categories
    for topic in TOPICS:
        for polarity in POLARITIES:
            cols    = _get_emotion_columns(df_data, topic, polarity)
            summed  = df_data[cols].sum(axis=1)

            p_r, p_val_r, s_r, s_val_r = _compute_corr(final_df["rating"], summed)
            p_a, p_val_a, s_a, s_val_a = _compute_corr(att_rating, summed)

            _print_corr(p_r, p_val_r, s_r, s_val_r,
                        f"Raw Rating vs {polarity.capitalize()} {topic}")
            _print_corr(p_a, p_val_a, s_a, s_val_a,
                        f"Adjusted Rating vs {polarity.capitalize()} {topic}")

            corr_records.extend([
                #uses TOPIC_DISPLAY_NAMES for the pretty label
                {"topic": TOPIC_DISPLAY_NAMES[topic], "polarity": polarity, "type": "Pearson",
                 "raw": p_r, "attuned": p_a},
                {"topic": TOPIC_DISPLAY_NAMES[topic], "polarity": polarity, "type": "Spearman",
                 "raw": s_r, "attuned": s_a},
            ])

        print("  " + "-" * 30)

    return pd.DataFrame(corr_records)


# ==============================================================================
# PLOT 1: Pearson + Spearman before/after bars
# ==============================================================================

def plot_correlation_changes(corr_df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    x_labels = corr_df["topic"].unique()
    x        = np.arange(len(x_labels))
    width    = 0.18

    fig, axes = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

    for ax, corr_type in zip(axes, ["Pearson", "Spearman"]):
        df_t = corr_df[corr_df["type"] == corr_type]

        pos_raw = df_t[df_t["polarity"] == "pos"]["raw"].values
        pos_att = df_t[df_t["polarity"] == "pos"]["attuned"].values
        neg_raw = df_t[df_t["polarity"] == "neg"]["raw"].values
        neg_att = df_t[df_t["polarity"] == "neg"]["attuned"].values

        ax.bar(x - 1.5 * width, pos_raw, width, label="Pos Raw",       color="palegreen")
        ax.bar(x - 0.5 * width, pos_att, width, label="Pos Adjusted", color="forestgreen")
        ax.bar(x + 0.5 * width, neg_raw, width, label="Neg Raw",       color="lightcoral")
        ax.bar(x + 1.5 * width, neg_att, width, label="Neg Adjusted", color="red")

        for xi, bars in enumerate(zip(pos_raw, pos_att, neg_raw, neg_att)):
            for j, val in enumerate(bars):
                va     = "bottom" if val >= 0 else "top"
                offset = 0.01    if val >= 0 else -0.01
                ax.text(
                    x[xi] + (j - 1.5) * width, val + offset,
                    f"{val:.2f}", ha="center", va=va, fontsize=8,
                )

        ax.set_title(f"{corr_type} Correlations Before and After Adjustment")
        ax.set_ylim(-0.6, 0.6)
        ax.legend()

    axes[0].set_ylabel("Pearson r")
    axes[1].set_ylabel("Spearman ρ")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(x_labels, rotation=0)
    axes[1].set_xlabel("Topics")
    plt.tight_layout()
    


# ==============================================================================
# PLOT 2: Weighted average % change in correlation magnitude
# ==============================================================================

def plot_weighted_pct_change(corr_df: pd.DataFrame) -> None:
    def _pct_change(raw, attuned):
        return (abs(attuned) - abs(raw)) * 100

    x_labels = corr_df["topic"].unique()
    records  = []

    for topic in x_labels:
        df_a = corr_df[corr_df["topic"] == topic]

        pearson_avg = (
            _pct_change(
                df_a[(df_a["type"] == "Pearson") & (df_a["polarity"] == "pos")]["raw"].values[0],
                df_a[(df_a["type"] == "Pearson") & (df_a["polarity"] == "pos")]["attuned"].values[0],
            ) +
            _pct_change(
                df_a[(df_a["type"] == "Pearson") & (df_a["polarity"] == "neg")]["raw"].values[0],
                df_a[(df_a["type"] == "Pearson") & (df_a["polarity"] == "neg")]["attuned"].values[0],
            )
        ) / 2

        spearman_avg = (
            _pct_change(
                df_a[(df_a["type"] == "Spearman") & (df_a["polarity"] == "pos")]["raw"].values[0],
                df_a[(df_a["type"] == "Spearman") & (df_a["polarity"] == "pos")]["attuned"].values[0],
            ) +
            _pct_change(
                df_a[(df_a["type"] == "Spearman") & (df_a["polarity"] == "neg")]["raw"].values[0],
                df_a[(df_a["type"] == "Spearman") & (df_a["polarity"] == "neg")]["attuned"].values[0],
            )
        ) / 2

        records.append({"topic": topic, "pearson_d": pearson_avg, "spearman_d": spearman_avg})

    df_pct = pd.DataFrame(records)
    x      = np.arange(len(df_pct))
    width  = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width / 2, df_pct["pearson_d"],  width, label="Pearson Change",  color="dodgerblue")
    ax.bar(x + width / 2, df_pct["spearman_d"], width, label="Spearman Change", color="orange")

    for xi, (p, s) in enumerate(zip(df_pct["pearson_d"], df_pct["spearman_d"])):
        for val, xpos in [(p, x[xi] - width / 2), (s, x[xi] + width / 2)]:
            va     = "bottom" if val >= 0 else "top"
            offset = 0.1     if val >= 0 else -0.1
            ax.text(xpos, val + offset, f"{val:.1f}%", ha="center", va=va, fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(df_pct["topic"], rotation=0)
    ax.set_ylabel("Average % Change in Correlation Magnitude")
    ax.set_title("Weighted Percentage Change in Correlations After Adjustment")
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin * 1.1, ymax * 1.1)
    ax.legend()
    plt.tight_layout()


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def run() -> None:
    
    print("\n=== Correlation Change Visualizations ===")
    print("  Loading data...")
    df     = pd.read_csv(FINAL_EMOTIONS)
    df_att = pd.read_csv(ATTUNED_RATINGS)

    
    df_data   = df.drop(columns=METADATA_COLS)
    df_data   = df_data[df_data[MISC_D_COL] > 0].reset_index(drop=True)
    final_df  = df_att.copy()

    print("  Computing correlations...")
    corr_df = build_corr_records(df_data, final_df)

    print("  Plotting correlation changes...")
    plot_correlation_changes(corr_df)

    print("  Plotting weighted % change...")
    plot_weighted_pct_change(corr_df)


    plt.show()

    
if __name__ == "__main__":
    run()