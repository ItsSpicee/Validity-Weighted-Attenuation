# Paper TODO

**Order of work:** rerun the pipeline and update the results → wait on the two
additional expert raters, then implement the confidence intervals and Fleiss'
kappa → write the 12-page paper. `handoff.md` in the project root records what
changed since the last full pipeline run and why.

The 12-page target constrains everything below. Every analysis added this session
*adds* length; see item 14 for the budget.

## Methodology and reproducibility

1. **Rerun the full pipeline after the missing-record preprocessing fix.** The
   five blank and unrated records are now excluded, producing an expected
   analytic corpus of 17,127 reviews. Regenerate all processed data, model
   outputs, validation results, and dependent figures before revising results.

2. ~~**Create a professor-level train/CV/test design.**~~ **Superseded — see
   "Early-stopping leak" below.** The defect this item named (the final test set
   selecting the stopping iteration) is fixed, but by removing early stopping
   rather than by adding a third professor partition. No train/CV/test redesign
   is needed; `professor_split` is unchanged.

3. **Rerun the full pipeline after the split change.** Regenerate the trained
   CatBoost model, feature importance, attenuation outputs, validation metrics,
   and all dependent figures and tables. **Still outstanding** — now also covers
   the early-stopping change below. Nothing has been rerun since that edit, so
   every model-derived number in the paper is currently stale.

4. **Update reported results and wording.** Replace the current final-model
   metrics and every downstream result affected by the rerun. Describe the
   resulting final test set as untouched only after the new design is in place.

## Early-stopping leak — code fixed 2026-08-21, paper not yet updated

### What was wrong

`train_final_model` passed the held-out test professors to CatBoost as an
`eval_set` with `early_stopping_rounds=50`. CatBoost trains on the training
rows but watches MAE on the `eval_set` and halts at its best iteration, so the
206 test professors selected the model's size and were then scored on it. The
reported MAE was therefore mildly optimistic. Confirmed live rather than
theoretical: `catboost_info/test_error.tsv` holds 877 rows against a 1000
iteration budget, so stopping did fire, and its final value 0.63697 is the
0.6369 reported in `tab:CatBoost-performance`.

This reached past Section 4.2. The truncated model is what `cat_boost_final.cbm`
stores, and `src/attenuation.py` loads it to compute every attenuation delta, so
the Section 4.3 held-out metrics were also produced by a model sized using those
same held-out rows.

`cross_validate` had the same shape one level down: each fold stopped on its own
validation split and was then scored on it. Confined to the training
professors — no test involvement — but the same double use, so the fold metrics
in `tab:CatBoost` carry the same bias.

Note that the professor-level split itself was never the problem.
`professor_split` reserved the test professors correctly and every stage honours
it; a single `fit` call handed them to CatBoost anyway.

### What was changed

Both `fit` calls now pass training rows only, and `early_stopping_rounds` is out
of `CATBOOST_PARAMS`, so every model runs the full fixed 1000 iterations and is
scored on rows that took no part in fitting.

- `src/regression.py` — `cross_validate` and `train_final_model`: dropped the
  `eval_set` and `early_stopping_rounds` arguments; docstrings record why.
- `constants.py` — removed `"early_stopping_rounds": 50` from `CATBOOST_PARAMS`;
  comment records why. `iterations` stays at 1000.

Deliberately not done: no inner validation partition, no CV-derived iteration
count, no seed averaging. The conventional three-way design costs ~20% of the
training professors to justify one integer, and the loss curve is flat over the
final iterations (0.63700 → 0.63698 → 0.63697), so stopping was buying
essentially nothing. CatBoost is instrumentation in this paper, not the result;
the fix is scaled to that.

The cost of the simpler fix is that 1000 has no data-derived justification. The
flat tail covers this, but it needs a sentence in Section 3.5 (below).

### Expected effect on results

Section 4.2 numbers should move very little — the flat tail means the removed
truncation was worth roughly 0.00003 MAE. The fold metrics should move slightly
more, since they carried the same bias with no offsetting change in training
size. Everything else changes because the model is no longer byte-identical, not
because it is materially worse.

**Sanity check when rerunning:** the CV mean is currently 0.6300 against a final
test MAE of 0.6369, i.e. cross-validation looks *better* than the final model.
That ordering is backwards — each fold trains on ~658 professors versus 823 for
the final model, so folds should score slightly worse. The inversion is the bias
showing. After the rerun the fold numbers should rise and land just above the
final test MAE. If the ordering stays inverted, something else is going on and
is worth chasing before writing the numbers up.

### Paper changes needed

Nothing here is done; all of it waits on the rerun in item 3.

| Location | Change |
|---|---|
| `main.tex:535` | Drop the "Early Stopping Rounds / 50" row from `tab:CatBoost-params` |
| `main.tex:523` | Weaken the hyperparameter-provenance claim — the exploratory CV that chose this configuration used the biased protocol. Say the configuration was fixed beforehand and not re-selected, rather than implying it was validated under the current one |
| `main.tex:543` | Describe fixed-iteration fitting instead of early stopping |
| `main.tex:545` | The claim "No professor contributes reviews to both parameter selection and reported evaluation" is now true as written. It was not before — verify it survives the rerun and keep it |
| §3.5 (new sentence) | State that the iteration count is fixed at 1000 with no early stopping, and that the loss curve is flat over the final iterations so the cap is not performing selection |
| `main.tex:767` | Rewrite for fixed-iteration fitting. Also: "controlling for overfitting across folds" is not what CV does here — it shows performance is consistent across professor subsets |
| `main.tex:769-785` | New fold table (`tab:CatBoost`) |
| `main.tex:1019` | New final MAE / ρ / R² (`tab:CatBoost-performance`) |
| `main.tex:1024` | Re-check "low absolute error … substantial explained variance" against the new numbers |
| `main.tex:568` | New `s` if the grid search moves it off 0.83 |
| §4.3, §4.4, §5.4 | Regenerated values throughout — see "Downstream" below |

### Downstream consequences of the rerun

Unchanged, and usable as fixed anchors: the 17,127-review corpus, all Section
4.1 ATC agreement results, every descriptive figure and `Diagrams/roberta/`,
the 823/206 professor split, the 3,414 / 2,052 / 77 reporting populations, and
the 10,380 (60.59%) adjusted-review count, which is a property of `misc_d > 0`
rather than of the model.

Regenerate: `Diagrams/SHAP/`, `Diagrams/correlations/`,
`Diagrams/adjustment_visuals/`, the Section 5.4 adjustment statistics
(mean Δ 0.0404, |Δ| 0.2072, max +2.6068 / −1.4581, min 2.84e−6 at
`main.tex:1029`), and the Section 3.9 worked examples in `ex1/ex2/ex3.tex`.
Run `Paper/worked_examples.py` afterwards — it is the only cross-file
consistency check and it is not wired into `pipeline.py`.

Two items need a decision rather than a rerun:

- **The model-comparison table (`main.tex:750-762`) has no generating code in
  this repo.** Nothing produces the Ordinal / Linear / RF / XGBoost / CatBoost
  row set, so the four baselines cannot be regenerated under the corrected
  protocol and CatBoost's 0.6492 there will not match anything else in the
  paper. The paper already carries three unexplained CatBoost MAEs (0.6492,
  0.6369, CV mean 0.6300). Decide between regenerating all five under one
  protocol and footnoting the table's provenance. Watch XGBoost's 0.6710: if
  the honest CatBoost MAE passes it, the selection argument at `main.tex:764`
  is contradicted by the paper's own table.
- **Section 4.4 is threshold-sensitive on a small sample.** `src/validation.py`
  bins the 77 expert pairs against `COARSE_DELTA_THRESHOLD = 0.5` and a fine
  window of `[0, 0.4]`. New deltas move pairs across the 0.5 boundary, so the
  coarse subset's *n*, its accuracy and its binomial p-value can shift
  discontinuously. This is the load-bearing evidence in the paper, so check it
  early in the rerun rather than last.

### Operational notes for the rerun

- `s` must be resolved in two passes: run with `--optimize-s`, then hand-edit
  `S_VALUE` in `constants.py` and rerun. `src/attenuation.py` only *warns* on
  divergence, it does not fail.
- `s` may move visibly. Per `handoff.md` it is weakly identified (SD 0.23 across
  resampling), while the resulting delta vectors still correlate 0.966–0.9995.
  A large-looking change in `s` with near-identical downstream results is the
  expected behaviour, not a bug — the Limitations section already sets this up.
- `src/attenuation.py` loads the saved `.cbm` from disk. Retraining without
  rerunning stages 5–6 and the plots leaves the CSVs and figures silently
  describing different models.
- The `Δ` in `_print_summary` still crashes on a cp1252 console when output is
  piped (see `handoff.md`). Set `PYTHONIOENCODING=utf-8` before a redirected
  run, or it can half-write the attuned CSVs.

## Robustness analyses — code added 2026-08-21, not yet run

Promoted out of `sidequestz/` into the pipeline as **stage 7**, `src/robustness.py`,
opt-in via `python pipeline.py --robustness`. Off by default because the
permutation control re-attenuates the corpus once per permutation. Outputs go to
`results/` as CSV plus `robustness_tables.tex`.

Both analyses load `cat_boost_final.cbm`, so **run them after the pipeline rerun**
(item 3), not before.

5. **Run the permutation control and write it into Section 4.3.** This is the
   highest-value addition available. Every current result in 4.3 shows the
   mechanism behaves as designed; none show the behaviour depends on a review's
   *actual* off-topic content, and an arbitrary review-specific adjustment would
   produce similarly structured correlations. Permuting `D_misc` is the control
   that separates them. Expect permuted accuracy near 0.5 and permuted
   correlations near 0.

   Note when writing it up that the null is "arbitrary density" rather than
   "density with realistic covariance" — permuting decouples `D_misc` from the
   emotion features, which pushes the model off the manifold it was trained on.
   A stratified permutation within rating bins would be the stronger null if a
   reviewer raises it.

6. **Run the sensitivity tables and write A and B into the paper.** Table A
   (delta agreement across `s`) and Table B (modulator correlations across `s`)
   are the defence if the rerun moves `s` off 0.83 — which is plausible, since
   it is weakly identified. Without them a visible change in `s` between drafts
   reads as instability rather than as a characterised property.

   Table C (expert accuracy across `s`) if there is space. It reports overall
   accuracy only, deliberately: the coarse and fine bins are defined by
   `delta_diff` thresholds that are themselves functions of `s`, so those columns
   would compare different subsets of pairs. State that reason explicitly if the
   table goes in.

   **Before running:** `SENSITIVITY_S_VALUES` in `constants.py` is `[0.37, 0.62,
   0.91]`, the modes from a resampling study run against the *old* model.
   Re-derive them after the rerun or the table compares the new `s` against
   values that no longer mean anything.

## Expert validation — deferred until the additional labels arrive

Two more experts are being recruited, taking Section 4.4 from one rater to three.
Everything in this block waits on those label files; nothing here is blocked on
anything else.

7. **Fold Wilson confidence intervals into `src/validation.py`.** Currently
   `sidequestz/expert_confidence_intervals.py`, kept there so it stays runnable
   against the single-expert file. `n = 77` is small enough that a reviewer will
   ask how stable the accuracy is; the interval answers it, and the claim to make
   in the text is that the lower bound clears 0.5.

   Expect the fine-grained condition's interval to straddle 0.5. Those are pairs
   the model nearly could not separate, so low accuracy there is the expected
   shape — accuracy rising with the size of the separation is itself evidence
   that `|Δ|` carries graded information. Write it that way rather than as an
   independent success.

8. **Add majority-vote label resolution to `src/validation.py`.** Rule: majority
   of *cast* votes; ties resolve to unsure; unsure stays counted as incorrect,
   matching the existing convention. Report how many pairs land in each bucket.

   **This must live in exactly one function that everything imports** — stage 6,
   the permutation control and sensitivity Table C all consume "what the expert
   said," and three copies of the rule will drift. Same failure mode
   `src/splits.py` was created to prevent for the professor split. Write it to
   auto-detect however many label columns are present so it runs unchanged with
   one expert or three.

9. **Report inter-rater agreement, and reframe 4.4 around it.** Three raters give
   mean pairwise agreement or Fleiss' kappa (roughly twenty lines, no new
   dependency). This matters more than it sounds: at present the model's accuracy
   is implicitly benchmarked against a 100% ceiling, which is the wrong
   comparison. If three trained experts agree with each other ~75% of the time,
   that is the ceiling. "The model agrees with expert consensus about as often as
   experts agree with one another" is a much stronger and more defensible claim
   than a bare accuracy figure, and it costs nothing beyond labels already being
   collected. Plan the 4.4 rewrite around it.

10. Confirm or document the three dropped expert pairs (`review_id` not found in
    attuned data: 14144/18846, 13330/678, 18844/7083), leaving 77 of 80. Likely
    `misc_d = 0` reviews and legitimately absent, but unconfirmed, and the paper
    mentions no exclusions.

## Other

11. Add explicit "full sample" labels to the external-validation and
    adjustment-outcomes tables for population-label consistency.

12. **Make the case against total exclusion explicit in Section 3.5.** The
    section asserts proportional attenuation is preferable to zeroing `E_misc`
    and leaves it at the Huber citation. Strengthen it with a clause noting that
    discarding forfeits the information in partially off-topic reviews and
    introduces a discontinuity at `D_misc = 0`.

    An empirical ablation was considered and **rejected**, for two reasons worth
    keeping on record. First, the validation metric is not scale-free: total
    exclusion produces larger deltas, larger deltas produce larger `delta_diff`,
    and larger `delta_diff` shifts pairs into the regime where the paired
    comparison is easy — so the comparison would partly reward aggressive
    attenuation for reasons unrelated to measurement quality, and "total
    exclusion scores higher" would be close to uninterpretable. Second,
    proportional down-weighting is a measurement-theoretic commitment following
    Huber's robust-estimation argument, not a hypothesis to settle by whichever
    variant maximises a downstream accuracy number; validating it that way would
    be optimising the wrong objective. The answer therefore stays principled.

    (For the record, it would have been nearly free: total exclusion is the
    `s → 0` limit of the existing family, since `zeta = 1 - D^s` tends to 0 for
    any `D > 0` as `s` tends to 0, so it is one extra row in the stage 7
    sensitivity tables. The decision is about what the test would mean, not what
    it would cost.)

13. **Length budget for the 12-page version.** This session added a permutation
    control, three sensitivity tables and confidence intervals, all of which add
    length to a paper that is already long. Decide early what earns space rather
    than cutting under deadline.

    Suggested priority if space is tight. The **permutation control** is the one
    addition that turns Section 4.3 from a description of designed behaviour into
    evidence, and it compresses to a short paragraph plus one small table — keep
    it. The **confidence intervals** are three extra columns in a table that
    already exists, so they cost almost nothing — keep them. **Sensitivity Table
    A** (delta agreement) is the defence if `s` moves in the rerun and can be
    reduced to a sentence with a range quoted inline. **Table B** duplicates much
    of Table A's message; drop to a clause if needed. **Table C** goes first.

    Candidates for compression on the other side: Section 3.9's three worked
    examples are prose-heavy and could become one example plus an appendix
    pointer, and the model-comparison table at `main.tex:750-762` may be dropped
    entirely if its provenance can't be resolved — which would also settle the
    orphaned-baselines problem noted under "Downstream consequences" above.

14. **Coarse/fine bin gap — fixed in code 2026-08-21, needs a paper sentence.**
    `FINE_DELTA_MAX` was 0.4 against a `COARSE_DELTA_THRESHOLD` of 0.5, so pairs
    with `delta_diff` in (0.4, 0.5) fell in neither bin and the two conditions
    did not partition the sample. `FINE_DELTA_MAX` now equals
    `COARSE_DELTA_THRESHOLD` and the fine bin is half-open, so every pair lands
    in exactly one. Section 4.4 should say the bins partition the pairs; check
    both bin `n`s after the rerun, since which one is small changes how the
    paragraph reads.
