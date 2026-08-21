# Session handoff

**Date:** 2026-08-21
**Branch:** `s-circularity-fix` (nothing committed)

Two rounds of work sit on this branch. The first closed a circularity in how the
down-weighting exponent `s` was selected; the second closed a leak in how the
CatBoost model chose its size, and promoted the robustness analyses into the
pipeline. **No results have been regenerated since either change.** Every
model-derived number in the paper is stale.

---

## Roadmap

1. **Rerun the pipeline and update the results.** Everything downstream of the
   model has to be regenerated. `Paper/todo.md` carries the itemised list,
   including the two items that need a decision rather than a rerun.
2. **Wait on the two additional expert raters,** then implement Wilson
   confidence intervals and Fleiss' kappa in `src/validation.py`.
3. **Write the 12-page paper.**

Note that (3) constrains (1) and (2): the robustness analyses added in this
session all *add* length. See the length-budget item in `Paper/todo.md`.

---

## Round 1 — `s` selection circularity (earlier sessions)

**The problem.** `s` was selected by a grid search whose loss is built from the
same correlation improvements the paper reports as results, and the search ran on
the full dataset. Two distinct issues: `s` was tuned on the rows it was then
evaluated on, and the loss *is* the reported metric, so those results partly
restated the objective regardless of which rows were used.

**Which results were in-criterion.** The correlation changes (4.3.2), the
modulator correlations (4.3.3) and the Mann-Whitney test are all terms in the
objective. SHAP (4.3.1) and the expert paired comparison (4.4) are not.

**`s` is weakly identified.** Resampling the tuning set over 20 professor-level
splits gave SD 0.23 and a range of 0.23–0.94, clustered into modes near 0.37,
0.62 and 0.91. Suspected cause: `ALPHA = 175.0` against `BETA = 2.0` amplifies
noisy correlation differences. Not investigated further.

**It doesn't matter downstream.** Across the modal range, delta vectors correlate
0.966–0.9995 with mean divergence under 0.09 rating points.

**Resolution: a two-way professor split.** With CatBoost and `s` both fit on
training professors, reporting on held-out professors means nothing that touched
the reported rows was fit to them. Rejected: a three-way split (a smaller tuning
set would worsen the already-poor identification of `s`) and a disclosure-only
patch.

- **`src/splits.py`** (new) — single source of truth for the professor-level
  split, so regression, s-tuning and reporting cannot drift apart.
- **`src/regression.py`** — both inline splits replaced with `professor_split()`.
- **`src/attenuation.py`** — `run()` tunes `s` on training professors only; both
  output CSVs gain an `is_heldout` column. `weighted_emotions.csv` is written
  after `s` is resolved and with that same `s`.
- **`constants.py`** — `S_VALUE = 0.83`; `REPORT_ON_HELDOUT` flag.
- **`src/visualizations/`** — §4.3 metrics restricted to held-out professors.
  Delta-distribution and professor-shift plots deliberately stay full-sample.

The remaining honest limitation is that `s` is weakly identified — the split
fixes the circularity, not the flat objective. This is stated in Limitations.

## Round 2 — early-stopping leak, and stage 7 (this session)

**The problem.** `train_final_model` passed the held-out test professors to
CatBoost as an `eval_set` with `early_stopping_rounds=50`. CatBoost trains on the
training rows but watches MAE on the `eval_set` and halts at its best iteration,
so the 206 test professors selected the model's size and were then scored on it.
Confirmed live, not theoretical: `catboost_info/test_error.tsv` holds 877 rows
against a 1000-iteration budget, and its final value 0.63697 is the 0.6369 in
`tab:CatBoost-performance`.

This reached past §4.2. The truncated model is what `cat_boost_final.cbm` stores,
and `src/attenuation.py` loads it to compute every delta, so the §4.3 held-out
metrics were produced by a model sized using those same held-out rows. It also
made `main.tex:545` false as written ("No professor contributes reviews to both
parameter selection and reported evaluation" — the iteration count is a selected
parameter).

`cross_validate` had the same shape one level down: each fold stopped on its own
validation split and was then scored on it. Confined to the training professors,
but the same double use, so the fold metrics carried the same bias.

The professor split itself was never the problem. `professor_split` reserved the
test professors correctly; one `fit` call handed them over anyway.

**Resolution: remove early stopping.** Both `fit` calls now pass training rows
only, and `early_stopping_rounds` is out of `CATBOOST_PARAMS`, so every model runs
a fixed 1000 iterations and is scored on rows that took no part in fitting.

A three-way train/CV/test design was considered and rejected as disproportionate:
it costs ~20% of the training professors to justify one integer, and the loss
curve is flat over the final iterations (0.63700 → 0.63698 → 0.63697), so
stopping was buying essentially nothing. CatBoost is instrumentation in this
paper, not the result. The cost is that 1000 has no data-derived justification;
the flat tail covers it, and §3.5 needs a sentence saying so.

**Stage 7 — `src/robustness.py`** (new). The permutation control and the
s-sensitivity tables were promoted out of `sidequestz/` into the pipeline,
opt-in via `python pipeline.py --robustness`. Off by default because the
permutation control re-attenuates the corpus once per permutation. Outputs to
`results/`.

**A bug was fixed during that move.** The original permutation test documented
that correlations are measured against the *true* `D_misc` but actually pulled
`misc_d` from the permuted frame — correlating permuted deltas against the
permuted densities that produced them. That re-measures the mechanism against its
own input and returns roughly the observed value at every permutation, so the
p-values would have come out near 1 and looked like the framework had failed.
True densities are now joined on `review_id`, which also holds the reporting
population fixed (permuting `D_misc` relocates the zeros, so the `D_misc > 0`
subset is otherwise a different set of rows in every permutation).

**Other changes.** `FINE_DELTA_MAX` now equals `COARSE_DELTA_THRESHOLD` with a
half-open fine bin, so the coarse and fine conditions partition the expert pairs
instead of leaving a gap at (0.4, 0.5). `merge_expert_deltas` was extracted from
`load_and_merge` in `src/validation.py` so stage 7 can score a frame directly
rather than round-tripping a temp CSV on every permutation.

---

## Expected effect of the rerun

§4.2 should move very little — the flat tail means the removed truncation was
worth roughly 0.00003 MAE. The fold metrics should move slightly more, since they
carried the same bias with no offsetting change in training size. Everything else
changes because the model is no longer byte-identical, not because it is
materially worse.

**Sanity check.** The CV mean is currently 0.6300 against a final test MAE of
0.6369 — cross-validation looks *better* than the final model. That ordering is
backwards: each fold trains on ~658 professors versus 823, so folds should score
slightly worse. The inversion is the bias showing. After the rerun the fold
numbers should rise and land just above the final test MAE. If the ordering stays
inverted, something else is going on.

**Populations** (unchanged by either round, usable as fixed anchors): 823 training
professors (13,718 reviews) / 206 held-out (3,414 reviews, of which 2,052 have
`misc_d > 0`). SHAP figures use 3,414; the correlation and modulator analyses use
2,052; §5.4 uses the full 10,380; §4.4 uses all 77 expert pairs. The 17,127-review
corpus and all §4.1 ATC results are model-independent and also unaffected.

## Operational notes for the rerun

- **`s` needs two passes.** Run with `--optimize-s`, hand-edit `S_VALUE` in
  `constants.py`, then rerun. `src/attenuation.py` only *warns* on divergence.
- **`s` may move visibly** and that is expected, not a bug — it is weakly
  identified while the downstream deltas are near-identical. Stage 7's Table A
  is the evidence for that sentence.
- **`SENSITIVITY_S_VALUES`** in `constants.py` is `[0.37, 0.62, 0.91]`, the modes
  from a resampling study run against the *old* model. Re-derive after the rerun.
- **Stage 7 loads the saved `.cbm`.** Run it after the pipeline, not before.
- **`src/attenuation.py` also loads the saved `.cbm`.** Retraining without
  rerunning stages 5–6 and the plots leaves CSVs and figures silently describing
  different models. `Paper/worked_examples.py` is the only cross-file consistency
  check and it is not wired into `pipeline.py`.
- **`Δ` in `_print_summary` crashes on a cp1252 console** when output is piped or
  redirected (`UnicodeEncodeError`). Fine interactively. It once killed a run
  *after* `weighted_emotions.csv` was written but *before* `attuned_ratings*.csv`
  — a half-written state. Workaround: `PYTHONIOENCODING=utf-8`. Fix: swap the `Δ`
  for ASCII in the print.

## Known issues, not fixed

**Three expert pairs are dropped** as `review_id` not found in attuned data
(14144/18846, 13330/678, 18844/7083), leaving 77 of 80. Probably `misc_d = 0`
reviews, legitimately absent — but unconfirmed, and the paper does not mention
any exclusions.

**The model-comparison table has no generating code.** Nothing in the repo
produces the Ordinal / Linear / RF / XGBoost / CatBoost rows at `main.tex:750-762`.
Those four baselines cannot be regenerated under the corrected protocol, and the
paper already carries three unexplained CatBoost MAEs (0.6492, 0.6369, CV mean
0.6300). Needs a decision, not a rerun — see `Paper/todo.md`.

## Repository layout notes

- **`sidequestz/`** now holds only `expert_confidence_intervals.py`, kept until
  the additional expert labels arrive and it folds into `src/validation.py`.
  The permutation test and sensitivity tables moved to `src/robustness.py`;
  `find_funny_reviews.py` (conference-slide quote mining) was deleted.
- **`Paper/worked_examples.py`** moved out of `sidequestz/`. Its import path
  still resolves — `Paper/` sits at the same depth `sidequestz/` did — but it now
  writes to `Paper/output/`.
- **`catboost_info/`** is committed and is a leftover of the last training run.
  Its `test_error.tsv` is the evidence for the early-stopping diagnosis above;
  once the rerun lands it is just noise and can be gitignored.
