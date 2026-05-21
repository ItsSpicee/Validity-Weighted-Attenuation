"""
src/attenuation.py
------------------
Stage 5: Validity-weighted attenuation and rating adjustment.

Produces:
  - weighted_emotions.csv      (down-weighted feature matrix)
  - attuned_ratings.csv        (reviews with misc_d > 0, adjusted ratings + deltas)
  - attuned_ratings_full.csv   (all reviews including those with misc_d == 0)
"""

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from scipy.stats import pearsonr, spearmanr

from constants import (
    CATBOOST_FINAL_MODEL,
    FINAL_EMOTIONS,
    WEIGHTED_EMOTIONS,
    ATTUNED_RATINGS,
    ATTUNED_RATINGS_FULL,
    METADATA_COLS,
    MISC_D_COL,
    POS_EMOTIONS,
    NEG_EMOTIONS,
    TOPICS,
    S_VALUE,
    S_SEARCH_MIN,
    S_SEARCH_MAX,
    S_SEARCH_STEP,
    ALPHA,
    BETA,
    DELTA,
    LAMBDA,
)




# ==============================================================================
# HELPERS
# ==============================================================================

def _corr_pair(x: pd.Series, y: pd.Series) -> dict:
    p, _ = pearsonr(x, y)
    s, _ = spearmanr(x, y)
    return {"Pearson": p, "Spearman": s}


def _sentiment_sum(df: pd.DataFrame, topic: str, polarity: str) -> pd.Series:
    base = POS_EMOTIONS if polarity == "pos" else NEG_EMOTIONS
    cols = [f"{e}_{topic}" for e in base if f"{e}_{topic}" in df.columns]
    return df[cols].sum(axis=1)


def _misc_intensity(df: pd.DataFrame, polarity: str) -> pd.Series:
    return _sentiment_sum(df, "misc", polarity)


def _apply_down_weighting(df: pd.DataFrame, s: float) -> pd.DataFrame:
    """Down-weight all *_misc emotion columns by (1 - misc_d^s)."""
    df_w = df.copy()
    misc_cols = [c for c in df_w.columns if "_misc" in c and c != MISC_D_COL]
    down_weighting = (1 - df_w[MISC_D_COL] ** s).values[:, None]
    df_w[misc_cols] *= down_weighting
    return df_w


# ==============================================================================
# S-value OPTIMIZATION (S value controls the down-weighting function)
# ==============================================================================

def optimize_s(
    model: CatBoostRegressor,
    df: pd.DataFrame,
    df_misc: pd.DataFrame,
    raw_preds: np.ndarray,
) -> float:
    """
    Grid search over [S_SEARCH_MIN, S_SEARCH_MAX] to minimize loss.

    #Maximizes decreases in correlation strength between raw misc emotions and adjusted ratings
    #Maximizes increase in correlation strength between raw pedagogical emotions and adjusted ratings
    #Maximizes correlations of attenuation delta with misc_d value 

    Loss = -ALPHA * ped_reward + BETA * misc_penalty - DELTA * align_reward
    """
    print("  Running grid search for optimal s...")

    s_values = np.arange(S_SEARCH_MIN, S_SEARCH_MAX, S_SEARCH_STEP)

    # Baseline correlations (raw rating vs. emotion sums)
    baseline_corrs: dict = {}
    for topic in TOPICS:
        baseline_corrs[topic] = {
            sent: _corr_pair(df_misc["rating"], _sentiment_sum(df_misc.drop(columns=METADATA_COLS), topic, sent))
            for sent in ("pos", "neg")
        }

    ped_topics = [a for a in TOPICS if a != "misc"]
    best_s, best_loss = S_VALUE, float("inf")
    results = []

    #original emotions
    X_misc = df_misc.drop(columns=METADATA_COLS)

    for s in s_values:
        df_w  = _apply_down_weighting(df_misc, s)
        X_w   = df_w.drop(columns=METADATA_COLS)
        w_preds = model.predict(X_w)
        delta   = w_preds - raw_preds
        att_rating = df_misc["rating"] + delta

        # Attuned correlations between original emotions and adjusted ratings
        att_corrs: dict = {}
        for topic in TOPICS:
            att_corrs[topic] = {
                sent: _corr_pair(att_rating, _sentiment_sum(X_misc, topic, sent))
                for sent in ("pos", "neg")
            }

        # Alignment reward
        abs_delta = np.abs(delta)
        p_align, _ = pearsonr(df_misc[MISC_D_COL], abs_delta)
        s_align, _ = spearmanr(df_misc[MISC_D_COL], abs_delta)
        align_reward = p_align + s_align

        # Pedagogical reward (with hinge)
        ped_terms = [
            max(att_corrs[a][sent][ct] - baseline_corrs[a][sent][ct], -LAMBDA)
            for a in ped_topics
            for sent in ("pos", "neg")
            for ct in ("Pearson", "Spearman")
        ]
        ped_reward = np.mean(ped_terms)

        # Misc leakage penalty
        misc_terms = [
            att_corrs["misc"][sent][ct] ** 2
            for sent in ("pos", "neg")
            for ct in ("Pearson", "Spearman")
        ]
        misc_penalty = np.mean(misc_terms)

        loss = -ALPHA * ped_reward + BETA * misc_penalty - DELTA * align_reward
        results.append({"s": round(s, 4), "loss": loss})

        if loss < best_loss:
            best_loss, best_s = loss, s

    print(f"  Optimal s = {best_s:.2f}  (loss = {best_loss:.4f})")
    return best_s


# ==============================================================================
# ATTENUATION
# ==============================================================================

def attenuate(
    model: CatBoostRegressor,
    df: pd.DataFrame,
    s: float,
) -> pd.DataFrame:
    """
    Apply validity-weighted attenuation and return a DataFrame with adjusted ratings.

    Adjusted rating = raw_rating + (attenuated_pred - baseline_pred)
    """
    meta_df  = df[METADATA_COLS].copy()
    df_data  = df.drop(columns=METADATA_COLS)

    # Baseline predictions
    raw_preds = model.predict(df_data)

    # Weighted predictions
    df_weighted = _apply_down_weighting(df, s)
    weighted_preds = model.predict(df_weighted.drop(columns=METADATA_COLS))

    delta = weighted_preds - raw_preds

    full_df = pd.concat(
        [
            meta_df,
            pd.Series(raw_preds,    name="original_pred"),
            pd.Series(weighted_preds, name="weighted_pred"),
            pd.Series(delta,          name="weighting_delta"),
            df[MISC_D_COL],
        ],
        axis=1,
    )
    return full_df


def _print_summary(full_df: pd.DataFrame, final_df: pd.DataFrame, total_n: int) -> None:
    inc = (final_df["weighting_delta"] > 0).sum()
    dec = (final_df["weighting_delta"] < 0).sum()
    abs_delta = final_df["weighting_delta"].abs()

    print(f"\n  Total ratings attuned:        {((inc + dec) / total_n) * 100:.2f}%")
    print(f"  Ratings increased:            {(inc / total_n) * 100:.2f}%")
    print(f"  Ratings decreased:            {(dec / total_n) * 100:.2f}%")
    print(f"  Max |Δ|:                      {abs_delta.max():.4f}")
    print(f"  Mean |Δ| (adjusted reviews):  {abs_delta.mean():.4f}")


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def run(find_optimal_s: bool = False) -> None:
    print("\n=== Stage 5: Attenuation ===")

    print("Loading model and data...")
    model = CatBoostRegressor()
    model.load_model(str(CATBOOST_FINAL_MODEL), format="cbm")

    df = pd.read_csv(FINAL_EMOTIONS)

    # Save down-weighted feature matrix
    df_weighted = _apply_down_weighting(df, S_VALUE)
    WEIGHTED_EMOTIONS.parent.mkdir(parents=True, exist_ok=True)
    df_weighted.to_csv(WEIGHTED_EMOTIONS, index=False)
    print(f"  Saved: {WEIGHTED_EMOTIONS}")

    # Subset: reviews with miscellaneous content
    df_misc = df[df[MISC_D_COL] > 0].reset_index(drop=True)
    X_misc_raw = df_misc.drop(columns=METADATA_COLS)
    raw_preds_misc = model.predict(X_misc_raw)

    # Optionally re-run grid search
    s = optimize_s(model, df_misc, df_misc, raw_preds_misc) if find_optimal_s else S_VALUE
    print(f"  Using s = {s}")

    # Run attenuation on full dataset
    full_df = attenuate(model, df, s)
    final_df = full_df[full_df[MISC_D_COL] > 0].reset_index(drop=True)

    # Attach misc emotion intensities
    X_misc_feat = df_misc.drop(columns=METADATA_COLS)
    final_df["misc_pos_intensity"] = _misc_intensity(X_misc_feat, "pos").values
    final_df["misc_neg_intensity"] = _misc_intensity(X_misc_feat, "neg").values
    final_df["total_misc_intensity"] = (
        final_df["misc_pos_intensity"] + final_df["misc_neg_intensity"]
    )

    _print_summary(full_df, final_df, total_n=len(df))

    final_df.to_csv(ATTUNED_RATINGS, index=False)
    full_df.to_csv(ATTUNED_RATINGS_FULL, index=False)
    print(f"  Saved: {ATTUNED_RATINGS}")
    print(f"  Saved: {ATTUNED_RATINGS_FULL}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimize-s", action="store_true")
    args = parser.parse_args()
    run(find_optimal_s=args.optimize_s)
