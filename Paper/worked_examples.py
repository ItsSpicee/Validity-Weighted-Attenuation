"""
Paper/worked_examples.py
------------------------
Recompute the Section 3.9 worked examples (Paper/.../ex1.tex, ex2.tex, ex3.tex)
at the current S_VALUE.

The examples were hand-traced at s = 0.86 and read as prose, so they are easy to
miss when regenerating figures. This prints, for each example review, the values
that depend on s alongside the values currently written in the paper, and emits
paste-ready LaTeX table bodies.

What depends on s
  - zeta = 1 - D_misc^s                        (Section 3 table, and the captions)
  - the down-weighted *_misc emotions          (Section 2, right-hand column)
  - baseline / attenuated preds, Delta, adjusted rating  (Section 3 table)

What does not
  - clause text, predicted topic, similarity, clause-level emotions (Section 1)
  - D_misc itself, and every non-misc topic row in Section 2

Section 1 is printed anyway as a cheap check that clause segmentation and ATC
did not shift when the pipeline was rerun.

DO NOT PASTE SECTION 1 INTO THE PAPER. Its clause text is un-anonymized and
carries real professor names where the paper writes [instructor]. Section 1 is
s-independent, so it is emitted as a diagnostic only; every value that belongs
in the .tex comes from Sections 2 and 3.

It also doubles as a cross-file consistency check: deltas are recomputed straight
from the model and compared against attuned_ratings_full.csv, warning if the
pipeline's outputs were produced at a different s. This caught the
S_VALUE-vs-tuned-s divergence before that bug was fixed and is worth keeping as a
tripwire. It is not wired into pipeline.py, so it has to be run deliberately.

`--s` regenerates at any exponent, which is how the harness was verified before
its output was trusted: running at the paper's previous s and diffing against the
committed .tex reproduced every s-independent value exactly.

Nothing here refits: the trained CatBoost model is loaded and used as-is, and
output goes only to Paper/output/.

Run from the project root, after the pipeline has finished:

    python Paper/worked_examples.py
    python Paper/worked_examples.py --s 0.83
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from constants import (  # noqa: E402
    ATTUNED_RATINGS_FULL,
    CATBOOST_FINAL_MODEL,
    CLAUSE_VECTORS,
    EMOTION_LABELS_NO_NEUTRAL,
    FINAL_EMOTIONS,
    METADATA_COLS,
    MISC_D_COL,
    S_VALUE,
    SIMILARITY_THRESHOLD,
    TOPIC_DESCRIPTIONS,
    TOPICS,
)
from src.attenuation import _apply_down_weighting  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "output"

# The three reviews traced in Section 3.9, in paper order.
EXAMPLES = [
    {"file": "ex1.tex", "label": "Worked Example 1", "review_id": 5},
    {"file": "ex2.tex", "label": "Worked Example 2", "review_id": 8113},
    {"file": "ex3.tex", "label": "Worked Example 3", "review_id": 14848},
]

# Values currently in the .tex files, traced at s = 0.86. Printed beside the new
# ones so a changed number is visible rather than inferred.
PAPER_S = 0.86
PAPER_VALUES = {
    5:     {"D_misc": 0.000, "zeta": 1.000, "raw": 5.0, "baseline": 5.003,
            "attenuated": 5.003, "delta":  0.000, "adjusted": 5.000},
    8113:  {"D_misc": 0.670, "zeta": 0.291, "raw": 3.0, "baseline": 2.506,
            "attenuated": 3.159, "delta":  0.653, "adjusted": 3.653},
    14848: {"D_misc": 0.450, "zeta": 0.497, "raw": 5.0, "baseline": 4.005,
            "attenuated": 3.743, "delta": -0.262, "adjusted": 4.738},
}

# Order of the per-clause similarity array in the clause vectors, and the display
# names used in the paper's tables.
SIM_TOPIC_ORDER = list(TOPIC_DESCRIPTIONS.keys())
DISPLAY = {
    "instructional_effectiveness": "Instr. Effectiveness",
    "fairness":                    "Fairness",
    "workload":                    "Workload",
    "misc":                        "\\textit{Miscellaneous}",
}

TOP_N_CLAUSE = 2   # Section 1 shows the top 2 emotions per clause
TOP_N_TOPIC  = 4   # Section 2 shows the top 4 per topic


# ==============================================================================
# HELPERS
# ==============================================================================

def _parse_sims(value) -> np.ndarray:
    """Per-clause topic similarities, stored as a stringified array (`[0.43 0.13 0.19]`)."""
    if isinstance(value, str):
        return np.fromstring(value.strip("[]"), sep=" ")
    return np.asarray(value, dtype=float)


def _zeta(d_misc: float, s: float) -> float:
    """The down-weighting multiplier applied to the *_misc block."""
    return 1.0 - d_misc ** s


def _top_emotions(values: pd.Series, n: int) -> str:
    """`emotion=0.123, ...` for the n largest non-zero entries, as the paper writes them."""
    nz = values[values > 0].sort_values(ascending=False).head(n)
    if nz.empty:
        return "---"
    return ", ".join(f"{name}={val:.3f}" for name, val in nz.items())


def _escape(text: str) -> str:
    """Minimal LaTeX escaping for clause text lifted from reviews."""
    for char in ("\\", "&", "%", "$", "#", "_", "{", "}"):
        text = text.replace(char, "\\" + char)
    return text


def _fmt_signed(x: float) -> str:
    """LaTeX-safe signed number: the paper writes $-$0.262 and +0.653."""
    return f"$-${abs(x):.3f}" if x < 0 else f"+{x:.3f}"


def _delta_note(new: float, old: float, tol: float = 5e-4) -> str:
    """Flag whether a value moved by more than a rounding step."""
    if abs(new - old) <= tol:
        return "unchanged"
    return f"CHANGED (was {old:+.3f}, moves {new - old:+.3f})"


# ==============================================================================
# SECTIONS
# ==============================================================================

def section1_clauses(clauses: pd.DataFrame) -> str:
    """
    Clause extraction and categorization. Independent of s.

    Emitted for verification only. The clause text here is raw and still contains
    professor names, which the paper replaces with [instructor] — do not paste
    this section into the .tex without re-anonymizing.
    """
    rows = []
    for _, clause in clauses.iterrows():
        sims = _parse_sims(clause["similarity"])
        # The paper's "Sim" column is the best topic similarity; a clause falls to
        # misc when that best score is below the ATC threshold.
        best_sim = float(sims.max())
        topic = clause["predicted_topic"]
        emotions = clause[EMOTION_LABELS_NO_NEUTRAL].astype(float)
        rows.append(
            f"{_escape(str(clause['review_clauses']))} & {DISPLAY[topic]} & "
            f"{best_sim:.3f} & {_top_emotions(emotions, TOP_N_CLAUSE)} \\\\"
        )
    return "\n\\addlinespace\n".join(rows)


def section2_vectors(row: pd.Series, s: float) -> tuple[str, dict]:
    """Baseline vs. down-weighted feature vector. Only the misc row changes."""
    d_misc = float(row[MISC_D_COL])
    zeta = _zeta(d_misc, s)

    rows, misc_cells = [], {}
    for topic in TOPICS:
        cols = {e: f"{e}_{topic}" for e in EMOTION_LABELS_NO_NEUTRAL}
        cols = {e: c for e, c in cols.items() if c in row.index}
        baseline = pd.Series({e: float(row[c]) for e, c in cols.items()})
        weighted = baseline * zeta if topic == "misc" else baseline

        baseline_txt = _top_emotions(baseline, TOP_N_TOPIC)
        weighted_txt = _top_emotions(weighted, TOP_N_TOPIC)
        if topic == "misc":
            # The paper prints the attenuated misc cell in red.
            misc_cells = {"baseline": baseline_txt, "weighted": weighted_txt}
            if weighted_txt != "---":
                weighted_txt = f"\\textcolor{{red}}{{{weighted_txt}}}"

        rows.append(f"{DISPLAY[topic]} & {baseline_txt} & {weighted_txt} \\\\")

    return "\n\\addlinespace\n".join(rows), misc_cells


def section3_attenuation(row: pd.Series, attuned: pd.Series, s: float) -> dict:
    """The attenuation summary row. Every column except Raw depends on s."""
    d_misc = float(row[MISC_D_COL])
    return {
        "D_misc":     d_misc,
        "zeta":       _zeta(d_misc, s),
        "raw":        float(attuned["rating"]),
        "baseline":   float(attuned["original_pred"]),
        "attenuated": float(attuned["weighted_pred"]),
        "delta":      float(attuned["weighting_delta"]),
        "adjusted":   float(attuned["rating"] + attuned["weighting_delta"]),
    }


# ==============================================================================
# CONSISTENCY CHECK
# ==============================================================================

def verify_against_model(
    model: CatBoostRegressor,
    df: pd.DataFrame,
    attuned: pd.DataFrame,
    s: float,
) -> None:
    """
    Recompute the example rows' predictions directly and compare to the pipeline's.

    Guards the known divergence risk in `attenuation.py`: the pipeline's
    `attuned_ratings_full.csv` is produced with whatever s `run()` used, which is
    the tuned value under `--optimize-s` and S_VALUE otherwise. If someone
    re-tunes s without updating the constant, these examples would silently
    describe a different s than the rest of the paper.
    """
    ids = [ex["review_id"] for ex in EXAMPLES]
    subset = df[df["review_id"].isin(ids)].reset_index(drop=True)

    raw_preds = model.predict(subset.drop(columns=METADATA_COLS))
    weighted = _apply_down_weighting(subset, s)
    weighted_preds = model.predict(weighted.drop(columns=METADATA_COLS))
    recomputed = pd.Series(weighted_preds - raw_preds, index=subset["review_id"])

    pipeline = attuned.set_index("review_id").loc[ids, "weighting_delta"]
    diff = (recomputed.loc[ids] - pipeline).abs().max()

    print(f"\nConsistency check — max |Delta_recomputed - Delta_pipeline| = {diff:.2e}")
    if diff > 1e-6:
        print(
            "  WARNING: the pipeline's attuned_ratings_full.csv was not produced at\n"
            f"  s = {s}. Re-run `python -m src.attenuation` after setting S_VALUE to\n"
            "  the tuned value, or these worked examples will contradict Section 4."
        )
    else:
        print(f"  OK — attuned_ratings_full.csv is consistent with s = {s}.")


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def main(s: float) -> None:
    print(f"=== Worked examples (Section 3.9) at s = {s} ===")
    print(f"Paper currently traces these at s = {PAPER_S}.")

    df = pd.read_csv(FINAL_EMOTIONS)
    attuned = pd.read_csv(ATTUNED_RATINGS_FULL)
    clause_vectors = pd.read_parquet(CLAUSE_VECTORS)
    print(f"  ATC similarity threshold: {SIMILARITY_THRESHOLD}")

    model = CatBoostRegressor()
    model.load_model(str(CATBOOST_FINAL_MODEL), format="cbm")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fragments = []

    for example in EXAMPLES:
        rid, label = example["review_id"], example["label"]
        row = df.loc[df["review_id"] == rid].squeeze()
        attuned_row = attuned.loc[attuned["review_id"] == rid].squeeze()
        clauses = clause_vectors[clause_vectors["review_id"] == rid]

        sec1 = section1_clauses(clauses)
        sec2, misc_cells = section2_vectors(row, s)
        sec3 = section3_attenuation(row, attuned_row, s)
        old = PAPER_VALUES[rid]

        print(f"\n{'=' * 78}\n{label} — review #{rid}  ({example['file']})\n{'=' * 78}")
        print(f"  clauses: {len(clauses)}   D_misc: {sec3['D_misc']:.3f} "
              f"(paper: {old['D_misc']:.3f})")
        print(f"\n  {'quantity':<12} {'new':>10} {'paper':>10}   note")
        for key in ("zeta", "raw", "baseline", "attenuated", "delta", "adjusted"):
            print(f"  {key:<12} {sec3[key]:>10.3f} {old[key]:>10.3f}   "
                  f"{_delta_note(sec3[key], old[key])}")

        print(f"\n  Section 2, misc row:")
        print(f"    baseline:      {misc_cells.get('baseline', '---')}")
        print(f"    down-weighted: {misc_cells.get('weighted', '---')}")

        pct = (1 - sec3["zeta"]) * 100
        print(f"\n  Caption facts: misc emotions down-weighted by {pct:.0f}% "
              f"(zeta = {sec3['zeta']:.3f}); "
              f"adjustment {'increases' if sec3['delta'] > 0 else 'decreases'} "
              f"the rating by {abs(sec3['delta']):.3f}.")

        fragments.append(
            f"% {'=' * 74}\n"
            f"% {label} — review #{rid} — regenerated at s = {s}\n"
            f"% Replace the three table bodies in {example['file']}.\n"
            f"% {'=' * 74}\n\n"
            f"% --- Section 1: Clause Extraction and Categorization (s-independent) ---\n"
            f"% NOT for pasting: clause text below is un-anonymized. The paper writes\n"
            f"% [instructor] in place of professor names.\n"
            f"{sec1}\n\n"
            f"% --- Section 2: Baseline vs. Attenuated Feature Vector ---\n"
            f"{sec2}\n\n"
            f"% --- Section 3: Validity-Weighted Attenuation ---\n"
            f"{sec3['D_misc']:.3f} & {sec3['zeta']:.3f} & {sec3['raw']:.1f} & "
            f"{sec3['baseline']:.3f} & {sec3['attenuated']:.3f} & "
            f"{_fmt_signed(sec3['delta'])} & \\textbf{{{sec3['adjusted']:.3f}}} \\\\\n"
        )

    verify_against_model(model, df, attuned, s)

    out_path = OUT_DIR / "worked_examples.tex"
    header = (
        f"% Regenerated by sidequestz/worked_examples.py at s = {s}\n"
        f"% Paper's ex1/ex2/ex3.tex were hand-traced at s = {PAPER_S}.\n"
        f"% Table bodies only — surrounding tabular/caption markup is unchanged.\n"
        f"% The captions quote zeta, the down-weighting percentage and Delta;\n"
        f"% update those by hand from the console output above.\n\n"
    )
    out_path.write_text(header + "\n".join(fragments), encoding="utf-8")
    print(f"\nSaved: {out_path}")
    print("Captions are prose and are NOT regenerated — update them by hand.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--s", type=float, default=S_VALUE,
        help=f"down-weighting exponent to trace the examples at (default: {S_VALUE})",
    )
    args = parser.parse_args()
    main(args.s)
