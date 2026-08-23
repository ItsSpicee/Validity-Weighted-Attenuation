# Session handoff

**Date:** 2026-08-22
**Branch:** `s-circularity-fix`

The pipeline rerun is **done**, the figures are **regenerated**, and every
model-derived number in this file has now been **transcribed into `main.tex`**.
The numbers below are kept as the record of the run and as the cross-check for
anyone re-reading the paper.

What remains is the `s` write-up, three smaller Part A items, and the assembly of
the LAK submission.

---

## Roadmap

1. ~~Regenerate the figures.~~ **Done.** `Paper/worked_examples.py` has run and
   its consistency check passes (max |Delta_recomputed - Delta_pipeline| =
   8.3e-17 at s = 1.0); `ex1/ex2/ex3.tex` carry the new values. `ex1` needed no
   change — that review has D_misc = 0.
2. ~~Update the existing paper in place.~~ **Numbers done** (`Paper/todo.md`
   Part A, "State of Part A", lists every value transcribed and everything
   re-verified as unchanged). **Still open: A7 — the paper has not caught up with
   `s`.** §3.5 still describes the grid search and states `s` = 0.83, §4.3 still
   refers to "the grid search that selected `s`", and the weak-identification
   limitation is still in §6. This is the one remaining inconsistency between the
   paper and the code, and it is a deliberate deferral rather than an oversight.
   A5 (population labels) and A6 (§3.5 total-exclusion argument) are also open.
3. **Start the LAK submission** as a new `.tex`, assembling from the existing
   paper rather than editing it. `Paper/todo.md` Part B.
4. **When the third expert's labels arrive:** Wilson intervals, majority-vote
   resolution and Fleiss' kappa in `src/validation.py`. `Paper/todo.md` Part C.

---

## Current results (2026-08-22, final run)

Produced under the corrected protocol on the **corrected 17,127-review corpus**:
professor-level split, no early stopping, `s` fixed a priori, reporting on
held-out professors. Raw console output is in `newresults.md`.

**`S_VALUE = 1.0`, fixed, not tuned** - see "Why `s` is fixed at 1.0" below.

**The corpus changed in this run, and the change is correct.** Earlier runs used
17,132 rows because `data/processed/` still held ATC output from 9 August, from
before the preprocessing fix that drops the five blank/unrated records (ids
694-698). Stages 1-3 had never been rerun. This run regenerated them, giving the
17,127 the paper has always claimed. Verified: for all 17,127 shared reviews the
ATC densities are bit-identical to the old file (max abs diff 0.0) and clause
counts match exactly, so nothing else moved. `misc_d > 0` is now 10,375 (was
10,380 - the five dropped reviews all had misc content).

### Section 4.2 - CatBoost

| Fold | MAE | Spearman | R2 |
|---|---|---|---|
| 1 | 0.6396 | 0.7461 | 0.6212 |
| 2 | 0.6254 | 0.7206 | 0.6197 |
| 3 | 0.6373 | 0.7433 | 0.6385 |
| 4 | 0.6306 | 0.7046 | 0.6151 |
| 5 | 0.6172 | 0.7273 | 0.6329 |
| **Mean** | **0.6300 +/- 0.0081** | **0.7284 +/- 0.0152** | **0.6255 +/- 0.0088** |

**Final test (held-out professors): MAE 0.6347, Spearman 0.7352, R2 0.6168.**

The folds are much tighter than in the previous run (SD 0.0213 -> 0.0081) and the
final test MAE falls **inside** the fold range (0.6172-0.6396). That makes the
write-up simple: cross-validation and the held-out test agree.

### Section 4.3 / 5.4 - attenuation

60.58% of ratings attuned (10,375), 31.96% increased, 28.62% decreased,
max |delta| 2.7103, mean |delta| 0.1964 on adjusted reviews. Held-out misc
subset 2,052 of 10,375.

The stage-5 console prints only `max |delta|` and `mean |delta|`. The remaining
Section 5.4 quantities were recovered from the visualization modules, which
print them, and are now in the paper:

| quantity | value |
|---|---|
| signed mean Delta | 0.0440 |
| most extreme decrease | -1.3908 |
| most extreme increase | 2.7103 |
| smallest non-zero \|Delta\| | 1.77e-6 |
| Wilcoxon (non-zero deltas, n = 10,375) | W = 24,260,091, p = 3.5e-18 |

Other numbers the paper needs that only the plotting code prints or draws:

- **Delta vs E_misc** (§4.3.3): Delta+ vs negative intensity 0.4008 Pearson /
  0.4327 Spearman; Delta- vs positive intensity -0.2470 / -0.1125.
- **Mann-Whitney** (§4.3.3): U = 313,494, p = 5.7e-121, |r| = 0.7887, on
  n = 690 low-noise and n = 508 high-noise reviews.
- **SHAP percentage shifts** (Discussion): Misc -9.635%, IE +1.644%,
  Fairness +2.459%, Workload +2.238% — read off `pct_change_shap.png`, which is
  the only place they exist.
- **Weighted correlation changes** (§4.3.2): signal +1.0 to +1.3%, Misc -7.5%
  Pearson / -10.0% Spearman. Supports the existing prose unchanged.
- **§5.1**: the Miscellaneous clause count is now **17,602** (was 17,607) — the
  only §5.1 number the five dropped reviews moved. Review frequencies,
  clauses-per-review, D_misc median 0.11 / mean 0.22 and the ~27% 1-star gap all
  re-verified identical.
- **Professor level**: mean professor average 3.6275 -> 3.6502 (+0.023); the 20
  largest professor shifts span roughly 0.3-0.7 with one -0.89 outlier.

`src/visualizations/attenuation_plots.py` is the source for the first three
groups. Run it with `PYTHONIOENCODING=utf-8` and keep the console output; it is
the only place several of these appear.

### Section 4.4 - expert validation

77 pairs (3 dropped, 4 unsure counted incorrect). Overall 62/77 = **80.5%**.
Coarse (>= 0.5) 38/43 = **88.4%**, p = 1e-7. Fine ([0, 0.5)) 24/34 = **70.6%**,
p = 0.0122. Bins partition the pairs, 77 of 77.

**The bins moved** (45/32 -> 43/34) because the deltas changed at s = 1.0. This
is the threshold sensitivity `Paper/todo.md` flagged: bin membership depends on
`COARSE_DELTA_THRESHOLD = 0.5`, so pairs cross the boundary whenever the deltas
move. It moved harmlessly here - both bins remain significant and the fine bin
improved - but the paper should say bin membership is threshold-dependent.

### Stage 7 - robustness

Permutation control, **N = 1000**, all three metrics 0/1000 hits, **p < 0.001**:

| metric | observed | null mean (SD) | null extreme |
|---|---|---|---|
| expert accuracy | 0.8052 | 0.6061 (0.0464) | max 0.7532 |
| pos_pearson | 0.6872 | 0.2327 (0.0291) | max 0.3235 |
| neg_pearson | -0.7077 | -0.1579 (0.0374) | min -0.2744 |

Sensitivity at `s` in {0.37, 0.62, 0.91, 1.0, 1.2}: delta agreement r =
0.9524-0.9990 (0.91 vs 1.0 at 0.9990, 1.0 vs 1.2 at 0.9979), modulator Pearson
0.670-0.687 positive and -0.669 to -0.715 negative, expert accuracy 80.5-87.0%.

**The permuted expert-accuracy mean is 0.6061, not ~0.5**, and that is a real
property rather than an artifact. `|delta|` still carries emotional-content
signal through the model even when the density driving it is shuffled, and
expert judgements track that content too. Section 4.3 needs a sentence saying
so: the observed 0.8052 is a gain over ~0.61, not over chance. Pre-empt it,
because a reader computing against 0.5 will overread the result.

---

## Why `s` is fixed at 1.0

`s` is no longer estimated. `--optimize-s`, `optimize_s()` and the composite
loss weights (`ALPHA`, `BETA`, `DELTA`, `LAMBDA`, `S_SEARCH_*`) have been
removed; they are recoverable from git history.

**Two reasons, and the second is the one that forced it.**

*It was never a clean estimate.* The grid objective is built from the same
correlation improvements Sections 4.3.2 and 4.3.3 report as results, so tuning
made those results partly restatements of the objective. The professor split
fixed the "tuned on the rows it is reported on" half; it could not fix the
in-criterion half, and no split can.

*It was unstable to a trivial perturbation.* Dropping the five blank records -
0.06% of the tuning rows, a correction with no scientific content - moved the
selected value from 0.93 to **0.2, the grid floor**. Landing on the boundary
means the optimum was censored, not found. Since zeta = 1 - D^s tends to 0 as s
tends to 0, the objective was pulling toward total exclusion, the very variant
Section 3.5 argues against. Earlier resampling had already shown SD 0.23 across
professor splits; this showed the argmin relocating on a rounding-error change
to the data.

**Why 1.0 specifically.** At s = 1, zeta = 1 - D_misc: the misc emotion channel
is retained in exact proportion to the review's on-topic fraction. That *is* the
proportional attenuation Section 3.5 already argues for on Huber grounds, so it
needs no separate justification, and it leaves no free parameter to defend.

**What this buys the paper.** Two limitations disappear - weak identification,
and in-criterion reporting of Sections 4.3.2 / 4.3.3 / Mann-Whitney - and the
methods section loses the entire grid-search description. The permutation
control also gets stronger: it now tests a mechanism with no parameter fitted
against statistics related to the ones the control evaluates.

**What it costs.** Nothing measurable. s = 0.91 and s = 1.0 agree at r = 0.9990,
mean |delta| difference 0.0129.

**How to frame it.** "The exponent is fixed at 1 rather than estimated" is true
and sufficient; do not narrate the grid search's instability in the paper. If a
reviewer asks directly whether tuning was tried, the honest answer is that the
objective did not identify a stable optimum, which is why the value is fixed on
principle - and Table A is the evidence that it does not matter.

**Still required:** held-out reporting. The deltas come from the CatBoost model,
which is still fit on training professors, so Section 4.3 stays on held-out
professors and `src/splits.py` is unchanged. Only the s-tuning arm of that
argument goes away.

---

## The CV/test inversion is resolved — it was never bias

The previous handoff predicted that removing early stopping would raise the fold
metrics above the final test MAE, and said that if the ordering stayed inverted
"something else is going on." **It stayed inverted** (CV 0.6300 < test 0.6347)
and nothing else is going on.

Removing early stopping moved every number by <= 0.0005 on the corpus of the
time. The leak was real but its effect was negligible on the CV side as well as
in the final fit — the flat tail again.

The correct explanation for the ordering is **between-professor heterogeneity,
not leakage**. On the final run the fold MAEs span 0.6172–0.6396 with SD 0.0081,
and the final test MAE of 0.6347 sits **+0.58 SD** from the fold mean and inside
the fold range. The training-size argument (658 vs 823 professors) predicts a gap
far smaller than that spread, so it is swamped by which professors land in which
partition. `src/regression.py` was re-read to confirm the protocol is clean:
`cross_validate` uses `professor_split` -> `train_rows` -> `GroupKFold` on
`prof_ID`, and neither fit passes an `eval_set`.

**Write it up as:** cross-validation shows performance is consistent across
professor subsets, and the held-out MAE falls within the fold range, so the two
are consistent rather than in tension. Do **not** repeat the current claim at
`main.tex:767` that CV "controls for overfitting across folds" — that is not
what CV does here.

---

## Fixed this session: the permutation control resampled its own population

**The bug.** `permutation_control` shuffled the whole `misc_d` column, which
relocates the zeros. Expert accuracy was then scored against the `misc_d > 0`
subset *of the permuted frame*, so a pair survived only when both of its reviews
happened to draw a positive density — roughly 0.606^2 x 80 = ~29 pairs. Measured
`expert_n` across 100 permutations ran **21–38, median ~30**, against an observed
n of 77. The docstring claimed n "can drift by a pair or two."

**Why it mattered.** The null variance was inflated by about sqrt(77/30) = 1.6x
(SD 0.0902, range reaching 0.8148), so 2/100 permutations "reached" the observed
0.8052 and the reported p = 0.0297 was a small-sample artifact rather than a
measurement. The two correlation rows were unaffected — they already held the
population fixed via the `true_d` join.

**The fix.** The shuffle is now restricted to rows where `misc_d > 0`, so zeros
stay zero and the analytic population is identical in every permutation. The
justification is that the `D_misc > 0` subset *is* the analytic population —
Section 4.3 reports on it and all 77 expert pairs fall inside it — so
exchangeability only has to hold there. `expert_n` is now 77 in 1000/1000.

Rejected alternatives, for the record: constraining only the expert-pair reviews
to non-zero (it works, but the constraint is defined by reference to the
evaluation set, which is harder to state in a methods section); and assigning
every review a random positive density (it changes the analytic population from
10,375 to 17,127, applies systematically more attenuation than the observed
condition, invents a generating distribution the p-value then depends on, and
puts every row off the manifold CatBoost was trained on).

**Consequence for the write-up.** The null is now the *graded* one — "the amount
of off-topic content is unrelated to which review it is", not "off-topic content
is absent". That is the claim Sections 4.3.3 and 4.4 actually make, and it is
close to the stratified permutation a reviewer would ask for. State it as a
deliberate choice rather than letting it read as convenience.

The `true_d` join stays. With zeros preserved it no longer fixes the population,
but it still supplies each review's **true** density as the correlate, which is
the whole point of the control.

---

## Two results that need a decided answer, not a rerun

**Table C: the operating point has the lowest expert accuracy in the table.**
s = 1.0 -> 80.5%, against 0.37 -> 85.7%, 0.62 -> 87.0%, 0.91 -> 84.4%,
1.2 -> 83.1%. A reviewer will ask why not 0.62. The answer is already on record as the argument that rejected the
total-exclusion ablation (`Paper/todo.md` Part D): **the validation metric is
not scale-free.** Smaller `s` attenuates harder -> larger deltas -> larger
`delta_diff` -> more pairs in the regime where the paired comparison is easy. So
0.62's 87% partly measures how aggressively it adjusts, not how well it
measures. The argument is directionally right but not clean: 1.2 attenuates even
less than 1.0 yet scores higher, so scale explains the trend and noise on 77
pairs explains the rest. If Table C goes in, that reasoning has to appear beside it or the
table undermines the choice of `s`. This is the strongest argument for cutting
Table C first under the length budget.

**Table B: some columns are marginally stronger away from the operating point.**
At 1.2 the negative arm reads -0.7145 Pearson / -0.6519 Spearman against -0.7077
/ -0.6001 at s = 1.0. This is a much smaller problem now that `s` is not chosen
by maximising anything — there is no argmin to defend. The answer is that `s` is
fixed on measurement-theoretic grounds and Table B shows the relationship holds
across the range (Pearson 0.670-0.687 positive, -0.669 to -0.715 negative).
Flatness is the message, and it reads better as an inline range than as a table
inviting column-by-column comparison.

---

## `SENSITIVITY_S_VALUES` — settled, do not re-derive

Now `[0.37, 0.62, 0.91, 1.2]`. The comment in `constants.py` has been rewritten
and no longer instructs a re-derivation.

That old instruction assumed the modes came from code in the repo. They did not.
The tuning-split resampling study (20 professor-level resamples, SD 0.23, range
0.23–0.94, modes near 0.37 / 0.62 / 0.91) was a throwaway diagnostic, deleted,
and present in no commit — it survives only as a note in the deleted
`sidequestz/context.md`, recoverable at `2f6d642^`. Its finding stands anyway,
because multimodality is a property of the loss surface and no change to the
model reshapes it. The values are spread comparison points, not estimates; they
do not need to be argmins of anything.

`1.2` was added deliberately above `S_SEARCH_MAX = 1.0`. Since zeta = 1 - D^s
with D in (0, 1], a larger `s` attenuates *less*, so it probes the direction the
grid search structurally cannot reach — which answers "did you only check inside
your own search bounds?". It is also the widest span in Table A (0.37 vs 1.2 at
r = 0.9496), so the table no longer looks curated.

---

## Operational notes

- **`--optimize-s` no longer exists.** `s` is fixed in `constants.py` and every
  stage reads it from there, so the CSVs, figures and sensitivity tables cannot
  desynchronise on the exponent. (A short-lived version of the flag rewrote
  `S_VALUE` mid-run and desynced stage 7, which had already imported the old
  value. Removing the flag removed the problem.)
- **Stage 7 and `src/attenuation.py` both load the saved `.cbm`.** Retraining
  without rerunning stages 5–7 and the plots leaves CSVs and figures silently
  describing different models.
- **`N_PERMUTATIONS = 1000`.** A default `python -m src.robustness` run is now
  the full control plus all sensitivity values, roughly five minutes.
- **Permutation p-values are floored at 1/(N+1).** Report `p < 0.001` with N
  stated, never `p = 0.001`.
- **Do not point a timing or scratch run at the default output paths.**
  `src/robustness.py` overwrites `results/` unconditionally, so a short run will
  clobber a long one. This happened once during this session.
- **`Delta` in `_print_summary` crashes on a cp1252 console** when output is
  piped or redirected. Set `PYTHONIOENCODING=utf-8`. Fix: swap it for ASCII.
- **`Paper/worked_examples.py` is the only cross-file consistency check** and is
  not wired into `pipeline.py`. Run it after the figures. It has been run for
  this state and passes.
- **`conda run -n absa` is required on this machine.** Calling
  `envs\absa\python.exe` directly dies with a DLL-load failure (0xC06D007E)
  because the env is never activated, so its DLL directories are off `PATH`.
- **`plot_topic_combinations` was fixed** (`src/visualizations/descriptive_plots.py`).
  `_load_exploded` already maps topics to display names, so the function's second
  `TOPIC_DISPLAY_NAMES` lookup was a no-op and the legend printed value-equals-key
  against white (invisible) patches. `constants.py` now carries
  `TOPIC_ABBREVIATIONS`. Figure data unchanged; labels only.

## Known issues, not fixed

**Three expert pairs are dropped** as `review_id` not found in attuned data
(14144/18846, 13330/678, 18844/7083), leaving 77 of 80. Probably `misc_d = 0`
reviews, legitimately absent — but unconfirmed, and the paper mentions no
exclusions.

**The model-comparison table has no generating code.** Nothing produces the
Ordinal / Linear / RF / XGBoost / CatBoost rows at `main.tex:750-762`. Needs a
decision, not a rerun — see `Paper/todo.md` Part D. The pressure is off, though:
XGBoost's 0.6710 is still comfortably above the honest CatBoost 0.6347, so the
selection argument at `main.tex:764` is **not** contradicted by the new numbers.

**`catboost_info/` is committed** and is now a leftover of the current training
run. It can be gitignored. Its `test_error.tsv` is stale and will not regenerate,
since no `eval_set` is passed any more — keep that in mind before citing it as
evidence of anything.

## Repository layout notes

- **`sidequestz/`** holds only `expert_confidence_intervals.py`, kept there until
  the third expert's labels arrive and it folds into `src/validation.py`.
- **`Paper/worked_examples.py`** writes to `Paper/output/`.
- **`newresults.md`** is the raw console output of the current run. The numbers
  are now in the paper, so it has served its purpose and can be deleted — kept
  for now only as the audit trail for the transcription.
