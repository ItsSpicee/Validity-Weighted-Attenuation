# Session handoff — s-parameter circularity fix

**Date:** 2026-08-07/08

## The problem

The down-weighting exponent `s` was selected by a grid search whose loss is built
from the same correlation improvements the paper reports as results, and the
search ran on the full dataset. Two distinct issues:

1. **Sample reuse** — `s` was tuned on the rows it was then evaluated on.
2. **Criterion reuse** — the loss *is* the reported metric, so those results
   partly restate the objective regardless of which rows are used.

The paper already conceded (1) in Limitations and promised to fix it in Future
Work.

## What we found

**Which results were in-criterion.** Mapping the loss (`attenuation.py`) onto
Section 4.3: the correlation changes (4.3.2), the modulator correlations
(4.3.3) and the Mann-Whitney test are all terms in the objective. SHAP (4.3.1)
and the expert paired comparison (4.4) are not. The load-bearing evidence — the
expert validation — was already clean.

**`s` is weakly identified.** Resampling the tuning set over 20 professor-level
splits gave SD 0.23 and a range of 0.23–0.94, clustered into modes near 0.37,
0.62 and 0.91. The loss surface has several near-equivalent minima and small
data perturbations flip which one wins. Suspected cause: `ALPHA = 175.0` against
`BETA = 2.0` amplifies noisy correlation differences. Not investigated further.

**It doesn't matter downstream.** Across the modal range, delta vectors correlate
0.966–0.9995 with mean divergence under 0.09 rating points; modulator
correlations stay flat (0.676–0.694); expert accuracy stays significant
everywhere (overall 0.79–0.86). Sensitivity checks reproduced the paper's
Section 4.4 numbers exactly at s = 0.86, confirming the harness was faithful.

**Tuning on training professors gives s = 0.83** — three grid steps from the
0.86 originally reported, so downstream numbers barely move.

## What we decided

A **two-way** professor split suffices; a third group is unnecessary. With
CatBoost and `s` both fit on training professors, reporting on held-out
professors means nothing that touched the reported rows was fit to them. `s` may
be mildly suboptimal there, but suboptimal-and-unbiased can only understate the
effect, never inflate it.

Rejected: re-tuning `s` on a smaller three-way split (would make the instability
worse, since a smaller tuning set gives a noisier estimate), and a
disclosure-only patch (unnecessary once 0.83 turned out to be so close).

## Code changes

- **`src/splits.py`** (new) — single source of truth for the professor-level
  split. `regression.py` previously built it inline in two places; drift between
  copies would have silently reintroduced the leak.
- **`src/regression.py`** — both inline splits replaced with `professor_split()`.
  Behaviour unchanged.
- **`src/attenuation.py`** — `run()` tunes `s` on training professors only;
  `optimize_s` lost an unused parameter and documents the training-rows
  requirement; both output CSVs gain an `is_heldout` column.
- **`constants.py`** — `S_VALUE = 0.83`; new `REPORT_ON_HELDOUT` flag.
- **`src/visualizations/correlation_plots.py`, `attenuation_plots.py`** — Section
  4.3 metrics restricted to held-out professors. Delta-distribution and
  professor-shift plots deliberately stay full-sample (descriptive, not
  validation). Expert validation in `src/validation.py` untouched, by design.

Verified: `python -m src.attenuation --optimize-s` selects 0.83 on 8,328 reviews
from 823 training professors, leaving 2,052 held-out misc reviews.

## Known issue, not fixed

`attenuation.py` writes `weighted_emotions.csv` using `S_VALUE` while
`attenuate()` uses the tuned `s`. Harmless while both are 0.83, but if a future
`--optimize-s` run returns something else, the SHAP figures (which read
`weighted_emotions.csv`) would silently describe a different `s` than the rest of
the paper. Pre-existing; worth fixing if `s` is ever re-tuned.

Cosmetic: `np.arange` makes `optimize_s` return `0.8300000000000005`. Differs
from `S_VALUE` by ~1e-15. `round(best_s, 2)` on the return would tidy it.

## State and next steps

Pipeline is non-circular end to end. Nothing has been regenerated yet and the
paper has not been touched.

1. **`Paper/todo.md`** — required paper changes. Highest priority is deleting the
   Future Work paragraph (~line 1175) promising to fix the circularity, which now
   contradicts the methodology. Also: "stratified" is used where "grouped" is
   meant, in five places.
2. Regenerate figures and numbers. Section 4.3 figures are held-out only now, so
   they must be regenerated rather than re-checked. The worked examples in
   Section 3.9 are hand-traced at s = 0.86 and read as prose — easy to miss.
3. **`sidequestz/`** — optional analyses (sensitivity tables, Wilson CIs,
   permutation control), none run yet. See `sidequestz/context.md`, which also
   documents what was deliberately excluded and why.

The remaining honest limitation is that `s` is weakly identified — the split
fixes the circularity, not the flat objective. `Paper/todo.md` item 1.2 has
suggested wording.
