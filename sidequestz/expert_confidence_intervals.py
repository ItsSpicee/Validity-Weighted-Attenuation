"""
sidequestz/expert_confidence_intervals.py
-----------------------------------------
Side-quest item 3: Wilson confidence intervals on the expert paired-comparison
accuracies reported in Section 4.4.

Rationale: n = 74 pairs is small, and a reviewer will notice. Reporting the
interval alongside the point estimate pre-empts that objection and costs
nothing. The intervals will be wide -- that is the honest picture, and stating
it is strictly better than leaving a reviewer to work it out.

Wilson is used rather than the normal-approximation (Wald) interval because Wald
behaves badly at proportions near 1 and at small n, both of which apply here.
Implemented directly to avoid adding a statsmodels dependency.

Reuses the pipeline's own merge and scoring so the accuracies here are exactly
the ones stage 6 reports.

Usage:
    python sidequestz/expert_confidence_intervals.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from constants import (  # noqa: E402
    COARSE_DELTA_THRESHOLD,
    EXPERT_LABELS_PATH,
    FINE_DELTA_MAX,
    FINE_DELTA_MIN,
)
from src.validation import load_and_merge, score_predictions  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "output"
CONFIDENCE = 0.95


def wilson_interval(correct: int, n: int, confidence: float = CONFIDENCE) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return float("nan"), float("nan")

    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    p = correct / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    halfwidth = z * ((p * (1 - p) / n + z**2 / (4 * n**2)) ** 0.5) / denom
    return max(0.0, centre - halfwidth), min(1.0, centre + halfwidth)


def main() -> None:
    if not Path(EXPERT_LABELS_PATH).exists():
        sys.exit(f"Expert labels not found at {EXPERT_LABELS_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    expert = score_predictions(load_and_merge())

    conditions = {
        "Overall": expert,
        f"Coarse ($\\geq {COARSE_DELTA_THRESHOLD}$)":
            expert[expert["delta_diff"] >= COARSE_DELTA_THRESHOLD],
        f"Fine ($\\leq {FINE_DELTA_MAX}$)":
            expert[expert["delta_diff"].between(FINE_DELTA_MIN, FINE_DELTA_MAX)],
    }

    rows = []
    for label, subset in conditions.items():
        n = len(subset)
        correct = int(subset["correct"].sum())
        lo, hi = wilson_interval(correct, n)
        p = stats.binomtest(correct, n, p=0.5, alternative="greater").pvalue if n else float("nan")
        rows.append({
            "Condition": label,
            "$n$": n,
            "Correct": correct,
            "Accuracy": correct / n if n else float("nan"),
            "95\\% CI": f"[{lo:.3f}, {hi:.3f}]",
            "$p$": p,
        })

    table = pd.DataFrame(rows)
    print(f"\n  Expert paired-comparison accuracy with {int(CONFIDENCE * 100)}% Wilson intervals\n")
    print(table.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    # A CI whose lower bound sits above 0.5 is the claim worth making in the
    # paper: agreement is above chance, not merely pointwise higher than it.
    print("\n  Lower bound above chance (0.5)?")
    for row, (_, subset) in zip(rows, conditions.items()):
        lo = float(row["95\\% CI"].strip("[]").split(",")[0])
        print(f"    {row['Condition']:<28} {'yes' if lo > 0.5 else 'NO'}  (lower = {lo:.3f})")

    table.to_csv(OUT_DIR / "expert_confidence_intervals.csv", index=False)
    latex = table.to_latex(index=False, escape=False, float_format="%.4f", column_format="lccccc")
    (OUT_DIR / "expert_confidence_intervals.tex").write_text(
        "\\begin{table}[htbp]\n\\centering\n"
        "\\caption{Expert paired-comparison accuracy with 95\\% Wilson confidence intervals.}\n"
        "\\label{tab:expert-ci}\n" + latex + "\\end{table}\n",
        encoding="utf-8",
    )
    print(f"\nSaved to {OUT_DIR}")


if __name__ == "__main__":
    main()
