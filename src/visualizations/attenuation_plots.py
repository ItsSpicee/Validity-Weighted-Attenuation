"""
src/visualizations/attenuation_plots.py
----------------------------------------
Visualizations for the validity-weighted attenuation results.

Produces:
  1. Attenuation Δ vs misc_d scatter plots (positive and negative Δ separately)
  2. SHAP feature importance bar charts (baseline vs attenuated)
  3. SHAP relative impact bar chart (% change after attenuation)
  4. SHAP beeswarm plot (aggregated emotion-topic features)
  5. Attenuation Δ frequency distribution histogram
  6. Professor average rating distribution shift (KDE)
  7. Largest professor average rating changes (bar chart)
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import shap
from scipy.stats import mannwhitneyu, wilcoxon
import catboost
from scipy.stats import pearsonr, spearmanr

from constants import (
    ATTUNED_RATINGS,
    ATTUNED_RATINGS_FULL,
    WEIGHTED_EMOTIONS,
    FINAL_EMOTIONS,
    CATBOOST_FINAL_MODEL,
    PROFESSORS_CLEANED,
    METADATA_COLS,
    POS_EMOTIONS,
    NEG_EMOTIONS,
    TOPICS,               
    TOPIC_DISPLAY_NAMES,  
)


TOPIC_COLORS = ["#1f77b4", "#ff7f0e", "#2fdb3d", "#d42222"]


# ==============================================================================
# HELPERS
# ==============================================================================

def _annotate_bars(ax, fmt="{:.3f}", offset=0.01) -> None:
    for bar in ax.patches:
        height = bar.get_height()
        if np.isnan(height):
            continue
        x  = bar.get_x() + bar.get_width() / 2
        y  = height + offset if height >= 0 else height - offset
        va = "bottom" if height >= 0 else "top"
        ax.text(x, y, fmt.format(height), ha="center", va=va, fontsize=9)


def _colour_beeswarm_labels(ax) -> None:
    for label in ax.get_yticklabels():
        text = label.get_text()
        if text.startswith("Positive"):
            label.set_color("#2e7d32")
            label.set_fontweight("bold")
        elif text.startswith("Negative"):
            label.set_color("#c62828")
            label.set_fontweight("bold")


# ==============================================================================
# 1. DELTA vs MISC_D SCATTER PLOTS
# ==============================================================================

def plot_delta_vs_misc_d(df_att: pd.DataFrame) -> None:
    df_pos = df_att[df_att["weighting_delta"] > 0].copy()
    df_neg = df_att[df_att["weighting_delta"] < 0].copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

    sns.scatterplot(
        data=df_pos, x="misc_d", y="weighting_delta",
        hue="misc_neg_intensity", palette="Reds", alpha=0.6, ax=ax1,
    )
    ax1.legend(title="Negative Emotional Intensity")
    sns.regplot(data=df_pos, x="misc_d", y="weighting_delta",
                scatter=False, color="darkred", ax=ax1)
    ax1.set_title("Positive Attenuation Δ's (Rating Increased)\nvs. Proportion of Miscellaneous Content")
    ax1.set_xlabel("Proportion of Miscellaneous Content")
    ax1.set_ylabel("Attenuation Δ")

    sns.scatterplot(
        data=df_neg, x="misc_d", y="weighting_delta",
        hue="misc_pos_intensity", palette="Greens", alpha=0.6, ax=ax2,
    )
    ax2.legend(title="Positive Emotional Intensity")
    sns.regplot(data=df_neg, x="misc_d", y="weighting_delta",
                scatter=False, color="darkgreen", ax=ax2)
    ax2.set_title("Negative Attenuation Δ's (Rating Decreased)\nvs. Proportion of Miscellaneous Content")
    ax2.set_xlabel("Proportion of Miscellaneous Content")
    ax2.set_ylabel("Attenuation Δ")

    plt.tight_layout()

    # Stats
    print("\n  --- Δ vs misc_d correlations ---")
    print(f"  Pos Δ vs misc_d  Pearson:  {pearsonr(df_pos['misc_d'], df_pos['weighting_delta'])[0]:.4f}")
    print(f"  Neg Δ vs misc_d  Pearson:  {pearsonr(df_neg['misc_d'], df_neg['weighting_delta'])[0]:.4f}")
    print(f"  Pos Δ vs misc_d  Spearman: {spearmanr(df_pos['misc_d'], df_pos['weighting_delta'])[0]:.4f}")
    print(f"  Neg Δ vs misc_d  Spearman: {spearmanr(df_neg['misc_d'], df_neg['weighting_delta'])[0]:.4f}")

    print("\n  --- Δ vs e_misc correlations ---")
    print(f"  Pos Δ vs neg intensity  Pearson:  {pearsonr(df_pos['misc_neg_intensity'], df_pos['weighting_delta'])[0]:.4f}")
    print(f"  Neg Δ vs pos intensity  Pearson:  {pearsonr(df_neg['misc_pos_intensity'], df_neg['weighting_delta'])[0]:.4f}")
    print(f"  Pos Δ vs neg intensity  Spearman: {spearmanr(df_pos['misc_neg_intensity'], df_pos['weighting_delta'])[0]:.4f}")
    print(f"  Neg Δ vs pos intensity  Spearman: {spearmanr(df_neg['misc_pos_intensity'], df_neg['weighting_delta'])[0]:.4f}")

    abs_delta_all = df_att["weighting_delta"].abs()
    misc_d = df_att["misc_d"]

    low_noise = abs_delta_all[(misc_d < 0.2) & (misc_d > 0)]
    high_noise = abs_delta_all[misc_d > 0.5]

    u_stat, u_p = mannwhitneyu(high_noise, low_noise, alternative='greater')
    r_rb = abs(1 - (2 * u_stat) / (len(high_noise) * len(low_noise)))

    print(f"\n  --- Mann-Whitney U (high vs low noise) ---")
    print(f"  Low noise  (Dmisc < 0.2): n={len(low_noise)}")
    print(f"  High noise (Dmisc > 0.5): n={len(high_noise)}")
    print(f"  U={u_stat:.0f}, p={u_p:.2e}, |r|={r_rb:.4f}")

# ==============================================================================
# 2. SHAP VISUALIZATIONS 
# ==============================================================================

def _get_agg_mass(explanation, feat_names: list[str]) -> dict:
    mass = {}
    # UPDATED: Use TOPICS list
    for topic in TOPICS:
        indices = [i for i, f in enumerate(feat_names) if f.endswith(f"_{topic}")]
        if indices:
            # UPDATED: Use TOPIC_DISPLAY_NAMES for lookup
            mass[TOPIC_DISPLAY_NAMES[topic]] = np.abs(explanation.values[:, indices]).sum(axis=1).mean()
    return mass


def _build_agg_explanation(explanation, feat_names: list[str]):
    agg_values, agg_data, agg_names = [], [], []
    # UPDATED: Use TOPICS list
    for topic in TOPICS:
        for polarity, emotions in (("Positive", POS_EMOTIONS), ("Negative", NEG_EMOTIONS)):
            # UPDATED: Use TOPIC_DISPLAY_NAMES for lookup
            group_name = f"{polarity}\n{TOPIC_DISPLAY_NAMES[topic]}"
            indices = [
                i for i, col in enumerate(feat_names)
                if any(col == f"{e}_{topic}" for e in emotions)
            ]
            if indices:
                agg_values.append(explanation.values[:, indices].mean(axis=1))
                agg_data.append(explanation.data[:, indices].mean(axis=1))
                agg_names.append(group_name)

    return shap.Explanation(
        values=np.column_stack(agg_values),
        data=np.column_stack(agg_data),
        feature_names=agg_names,
        base_values=explanation.base_values,
    )


def plot_shap(
    model: catboost.CatBoostRegressor,
    df_unweighted: pd.DataFrame,
    df_weighted: pd.DataFrame,
) -> None:
    X_u = df_unweighted.drop(columns=METADATA_COLS)
    X_w = df_weighted.drop(columns=METADATA_COLS)
    feat_names = X_u.columns.tolist()

    explainer  = shap.Explainer(model)
    shap_ex_u  = explainer(X_u)
    shap_ex_w  = explainer(X_w)

    mass_u = _get_agg_mass(shap_ex_u, feat_names)
    mass_w = _get_agg_mass(shap_ex_w, feat_names)

    # --- Grouped bar chart ---
    fig, ax = plt.subplots(figsize=(8, 5))
    df_mass = pd.DataFrame({"Baseline": mass_u, "Attenuated": mass_w}).T
    # UPDATED: Use TOPIC_COLORS
    df_mass.plot(kind="bar", ax=ax, color=TOPIC_COLORS)

    plt.ylabel("Mean |SHAP| contribution")
    plt.title("Importance by Category (Baseline vs Attenuated)")
    plt.xticks(rotation=0)
    _annotate_bars(ax, fmt="{:.3f}")
    plt.tight_layout()

    # --- Delta bar chart ---
    fig, ax = plt.subplots(figsize=(8, 5))
    delta = ((df_mass.loc["Attenuated"] - df_mass.loc["Baseline"]) / df_mass.loc["Baseline"]) * 100
    # UPDATED: Use TOPIC_COLORS
    delta.plot(kind="bar", ax=ax, color=TOPIC_COLORS)

    plt.axhline(0, color="black", linewidth=0.8)
    plt.ylabel("% Change in Mean |SHAP|")
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin * 1.05, ymax * 1.05)
    plt.title("Relative Impact of Attenuation on Feature Importance")
    plt.xticks(rotation=0)
    _annotate_bars(ax, fmt="{:+.3f}%", offset=0.002)
    plt.tight_layout()

    # --- Beeswarm ---
    agg_shap_u = _build_agg_explanation(shap_ex_u, feat_names)
    n_features  = len(agg_shap_u.feature_names)

    plt.figure(figsize=(14, 1.2 * n_features))
    shap.plots.beeswarm(agg_shap_u, show=False)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.1)
    ax = plt.gca()
    ax.tick_params(axis="y", labelsize=11)
    _colour_beeswarm_labels(ax)
    plt.tight_layout()


# ==============================================================================
# 3. ATTENUATION DELTA DISTRIBUTION  
# ==============================================================================

def plot_delta_distribution(df_att: pd.DataFrame, df_full: pd.DataFrame) -> None:
    deltas     = df_att["weighting_delta"]
    mean_delta = deltas.mean()

    plt.figure(figsize=(10, 6))
    sns.histplot(deltas, kde=True, bins=30, color="purple", alpha=0.6)
    plt.axvline(0, color="black", linestyle="--", linewidth=1, label="No Change")
    plt.axvline(mean_delta, color="red", linestyle="-", linewidth=2,
                label=f"Mean Δ: {mean_delta:.4f}")
    plt.title("Frequency Distribution of Attenuation Δs", fontsize=14)
    plt.xlabel("Attenuation Δ", fontsize=12)
    plt.ylabel("Number of Reviews", fontsize=12)
    plt.legend()
    plt.text(deltas.min(), plt.ylim()[1] * 0.8, "← Rating Decreased",
             color="darkred", fontweight="bold")
    plt.text(deltas.max() * 0.5, plt.ylim()[1] * 0.8, "Rating Increased →",
             color="darkgreen", fontweight="bold")
    plt.tight_layout()

    abs_deltas = deltas.abs()
    print("\n  --- Adjustment summary ---")
    print(f"  Total attuned:              {len(deltas)}")
    print(f"  % of all reviews:           {len(deltas) / len(df_full) * 100:.2f}%")
    print(f"  Average Δ:                  {mean_delta:.4f}")
    print(f"  Average |Δ|:                {abs_deltas.mean():.4f}")
    print(f"  Most extreme decrease:      {deltas.min():.4f}")
    print(f"  Most extreme increase:      {deltas.max():.4f}")
    print(f"  Smallest |Δ|:               {abs_deltas[abs_deltas > 0].min():.16f}")

    delta_all = df_full["weighting_delta"].copy()
    
    nonzero_mask = delta_all != 0
    nonzero_delta = delta_all[nonzero_mask]

    # Overall Wilcoxon on signed non-zero deltas
    w_res = wilcoxon(nonzero_delta)
    n = len(nonzero_delta)
    
    print(f"Wilcoxon Signed-Rank Test (non-zero deltas, n={n})")
    print(f"  W={w_res.statistic:.0f}, p={w_res.pvalue:.2e}")
    


# ==============================================================================
# 4. PROFESSOR-LEVEL RATING SHIFT  
# ==============================================================================

def plot_professor_shifts(df_full: pd.DataFrame, df_prof: pd.DataFrame) -> None:
    df_full["att_rating"] = (df_full["rating"] + df_full["weighting_delta"]).clip(1.0, 5.0)

    prof_att = df_full.groupby("prof_ID").agg(att_rating=("att_rating", "mean")).reset_index()
    df_prof  = df_prof.merge(prof_att, on="prof_ID", how="left")
    df_prof["delta"] = df_prof["att_rating"] - df_prof["average_rating"]

    df_prof.to_csv("data/processed/prof_with_att_average.csv", index=False)

    # KDE plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(df_prof["average_rating"], label="Original Rating",
                fill=True, color="skyblue", bw_adjust=0.8)
    sns.kdeplot(df_prof["att_rating"], label="Adjusted Rating",
                fill=True, color="orange", bw_adjust=0.8)
    plt.axvline(df_prof["average_rating"].mean(), color="blue", linestyle="--",
                label="Original Mean")
    plt.axvline(df_prof["att_rating"].mean(), color="red", linestyle="--",
                label="Adjusted Mean")
    plt.title("Professor Average Rating Distribution Shift (Raw vs. Adjusted)")
    plt.xlabel("Rating (1-5)")
    plt.legend()

    # Top/bottom bar chart
    df_sorted = df_prof.sort_values("delta", ascending=False)
    df_sorted["prof_ID"] = df_sorted["prof_ID"].astype(str)
    top_bottom = pd.concat([df_sorted.head(10), df_sorted.tail(10)])
    top_bottom = top_bottom.sort_values("delta")
    plt.figure(figsize=(10, 6))
    colors = ["#2ca02c" if x > 0 else "#d62728" for x in top_bottom["delta"]]
    plt.barh(top_bottom["prof_ID"], top_bottom["delta"], color=colors)
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Largest Changes in Professor Average Ratings (Positive and Negative)")
    plt.xlabel("Professor Average Rating Change")
    plt.ylabel("Professor ID")
    plt.grid(axis="x", linestyle="--", alpha=0.6)



# ==============================================================================
# ENTRY POINT
# ==============================================================================

def run() -> None:
    print("\n=== Attenuation Visualizations ===")

    print("  Loading data...")
    df_att   = pd.read_csv(ATTUNED_RATINGS)
    df_full  = pd.read_csv(ATTUNED_RATINGS_FULL)
    df_u     = pd.read_csv(FINAL_EMOTIONS)
    df_w     = pd.read_csv(WEIGHTED_EMOTIONS)
    df_prof  = pd.read_csv(PROFESSORS_CLEANED)

    model = catboost.CatBoostRegressor()
    model.load_model(str(CATBOOST_FINAL_MODEL), format="cbm")

    print("  Plotting Δ vs misc_d...")
    plot_delta_vs_misc_d(df_att)

    print("\n  Plotting SHAP (this may take a moment)...")
    plot_shap(model, df_u, df_w)

    print("\n  Plotting Δ distribution...")
    plot_delta_distribution(df_att, df_full)

    print("\n  Plotting professor-level shifts...")
    plot_professor_shifts(df_full, df_prof)

    

    plt.show()


if __name__ == "__main__":
    run()