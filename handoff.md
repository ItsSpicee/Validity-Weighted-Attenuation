# Session handoff — s-parameter circularity fix

**Date:** 2026-08-07/09
**Branch:** `s-circularity-fix` (nothing committed as of the last session)

## The problem

The down-weighting exponent `s` was selected by a grid search whose loss is built
from the same correlation improvements the paper reports as results, and the
search ran on the full dataset. Two distinct issues:

1. **Sample reuse** — `s` was tuned on the rows it was then evaluated on.
2. **Criterion reuse** — the loss *is* the reported metric, so those results
   partly restate the objective regardless of which rows are used.

## What was found

**Which results were in-criterion.** The correlation changes (4.3.2), the
modulator correlations (4.3.3) and the Mann-Whitney test are all terms in the
objective. SHAP (4.3.1) and the expert paired comparison (4.4) are not. The
load-bearing evidence — the expert validation — was already clean.

**`s` is weakly identified.** Resampling the tuning set over 20 professor-level
splits gave SD 0.23 and a range of 0.23–0.94, clustered into modes near 0.37,
0.62 and 0.91. Suspected cause: `ALPHA = 175.0` against `BETA = 2.0` amplifies
noisy correlation differences. Not investigated further.

**It doesn't matter downstream.** Across the modal range, delta vectors correlate
0.966–0.9995 with mean divergence under 0.09 rating points.

## What was decided

A **two-way** professor split. With CatBoost and `s` both fit on training
professors, reporting on held-out professors means nothing that touched the
reported rows was fit to them. Rejected: a three-way split (a smaller tuning set
would worsen the already-poor identification of `s`) and a disclosure-only patch.

## State: complete

**Pipeline** is non-circular end to end, at `s = 0.83`.

**Paper** is numerically and textually consistent with it. All values, tables,
figures and prose updated; figures regenerated into `Paper/.../Diagrams/`;
`ex2.pdf`/`ex3.pdf` recompiled. See `Paper/todo.md` for the itemised record and
the short remaining list.

### Code changes

- **`src/splits.py`** (new) — single source of truth for the professor-level
  split, so regression, s-tuning and reporting cannot drift apart.
- **`src/regression.py`** — both inline splits replaced with `professor_split()`.
- **`src/attenuation.py`** — `run()` tunes `s` on training professors only; both
  output CSVs gain an `is_heldout` column. **The `S_VALUE`-vs-tuned-`s`
  divergence noted in the previous handoff is fixed:** `weighted_emotions.csv` is
  now written after `s` is resolved and with that same `s`, the tuned value is
  rounded to the grid step, and a warning fires if it differs from `S_VALUE`.
  `S_VALUE` is now only the default for non-tuning runs.
- **`constants.py`** — `S_VALUE = 0.83`; `REPORT_ON_HELDOUT` flag.
- **`src/visualizations/`** — §4.3 metrics restricted to held-out professors.
  Delta-distribution and professor-shift plots deliberately stay full-sample.
  `validation.py` (expert comparison) untouched, by design.
- **`sidequestz/worked_examples.py`** (new) — recomputes the Section 3.9 worked
  examples at the current `s` and diffs against the values in the paper. Also
  serves as a cross-file consistency check: it recomputes deltas from the model
  and compares them to `attuned_ratings_full.csv`. Currently 0.00e+00.

### Populations

Split: 823 training professors (13,718 reviews) / 206 held-out (3,414 reviews,
of which 2,052 have `misc_d > 0`). SHAP figures use 3,414; the correlation and
modulator analyses use 2,052; §5.4 uses the full 10,380; §4.4 uses all 77 expert
pairs.

## Known issues, not fixed

**`Δ` in `_print_summary` crashes on a cp1252 console when output is piped or
redirected** (`UnicodeEncodeError`). Fine interactively. It killed one run
*after* `weighted_emotions.csv` was written but *before* `attuned_ratings*.csv`
— a half-written state. Workaround: `PYTHONIOENCODING=utf-8`. Fix: swap the `Δ`
for ASCII in the print.

**Three expert pairs are dropped** as `review_id` not found in attuned data
(14144/18846, 13330/678, 18844/7083), leaving 77 of 80. Probably `misc_d = 0`
reviews, legitimately absent — but unconfirmed, and the paper does not mention
any exclusions.

## Next steps

1. **Commit.** Nothing on this branch is committed.
2. **`Paper/todo.md` remaining list** — chiefly confirming the §4.2/§5.3
   regression numbers, which were assumed unchanged but never checked.
3. **`sidequestz/`** — three optional analyses, none run. The permutation control
   is the highest-value one. See `sidequestz/context.md`.

The remaining honest limitation is that `s` is weakly identified — the split
fixes the circularity, not the flat objective. This is now stated in the paper's
Limitations rather than promised as future work.
