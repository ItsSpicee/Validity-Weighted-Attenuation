# sidequestz

Optional analyses. None of these are required for the framework to work or for
the paper to be correct — they are additions worth including **if there is space**,
each chosen for high reviewer impact relative to the effort of running it.

Nothing here modifies the pipeline. Every script loads the trained model, never
refits, and writes only into `sidequestz/output/`.

Run from the project root:

```
python sidequestz/sensitivity_across_s.py
python sidequestz/expert_confidence_intervals.py
python sidequestz/permutation_test.py
```

---

## The scripts

### `sensitivity_across_s.py` — items 1, 2, 6

Robustness of the framework to the down-weighting exponent `s`. Produces three
tables, as CSV and as LaTeX (`output/sensitivity_tables.tex`).

- **Table A — delta agreement.** Pairwise correlation between the attenuation
  deltas produced at different `s` values. Earlier runs gave Pearson 0.966–0.9995
  with mean divergence under 0.09 rating points, i.e. the mechanism does
  substantially the same thing across the whole plausible range.
- **Table B — modulator correlations.** Section 4.3.3's delta-vs-`D_misc`
  correlations recomputed at each `s`. Previously flat (0.676–0.694), so the
  headline result is not an artifact of the tuned value.
- **Table C — expert accuracy.** Section 4.4's paired-comparison accuracy at
  each `s`.

Tables A and B use held-out professors, matching the Section 4.3 convention.
Table C uses the full sample, because the expert pairs span all professors and
restricting them would leave too few to be informative.

**Table C reports overall accuracy only, and this is deliberate.** The coarse and
fine bins are defined by `delta_diff` thresholds that are themselves functions of
`s`, so bin membership shifts between settings and those columns would compare
different subsets of pairs rather than the same pairs under different treatment.
Overall keeps `n` fixed and is the only apples-to-apples comparison available.
If the table goes in the paper, state that reason explicitly — it is a genuine
methodological point, and it also happens to avoid presenting a fine-grained
column that swings with `s` for reasons that are partly artefactual.

### `expert_confidence_intervals.py` — item 3

Wilson 95% confidence intervals on the Section 4.4 accuracies. `n = 74` is small
and a reviewer will notice; reporting the interval pre-empts the objection.

The intervals will be wide. That is the honest picture, and stating it is better
than having someone else compute it. The claim worth making is that the lower
bound sits above chance — the script prints that check explicitly. Watch the
fine-grained condition in particular; it is the one most likely to have a lower
bound near or below 0.5.

Wilson rather than the normal-approximation interval, because the latter
misbehaves at proportions near 1 and at small `n`, both of which apply.

### `permutation_test.py` — item 5

The strongest addition of the three, and the one the methodology arguably should
have had from the start.

Every result in Section 4.3 shows the mechanism behaves as designed, but none of
them show the behaviour depends on a review's *actual* off-topic content. A
mechanism assigning arbitrary review-specific adjustments would also produce
structured-looking correlations. This is the control that separates the two.

`D_misc` is permuted across reviews — breaking the correspondence between
measured density and applied attenuation while leaving every marginal
distribution intact — and expert accuracy plus the modulator correlations are
recomputed. Correlations are measured against *true* `D_misc`, since that is the
relationship the paper claims.

Expect permuted accuracy to collapse toward 0.5 and the correlations toward 0.
`D_misc` is permuted in the feature matrix as well as in the down-weighting term,
since it is both a model input and the driver of zeta; permuting only one would
leave a back-channel for true density to influence the adjustment.

Default is 100 permutations. Reduce with `--n-permutations` if it is slow.

---

## Notes

**Expected exposure.** Items 1, 2, 3 and 5 are uniformly favourable — there is no
plausible outcome that weakens the paper. Item 6 is favourable as scoped above,
but reporting the full coarse/fine breakdown across `s` would surface a
fine-grained accuracy that degrades at high `s`. The scoping is defensible on its
own merits, but it is a choice, and worth making knowingly.

**Deliberately not included: the loss-versus-`s` curve.** The `s` selection
procedure has several near-equivalent local minima, which is why resampling the
tuning set moves the selected value around. Plotting the curve advertises that
directly. Table A conveys the useful half of the message — the choice does not
matter much downstream — without drawing attention to the soft spot. This is a
presentation judgement, not a correctness one: the multimodality is real, and if
a reviewer asks, the honest answer is that the objective does not uniquely
identify `s` and the sensitivity tables are why that is acceptable.

**Also considered, not implemented: an ablation against total exclusion.**
Section 3 asserts that proportional attenuation is preferable to zeroing out
`E_misc` entirely, but never tests it. That test is roughly twenty lines and
would be the single strongest addition available *if* proportional attenuation
wins. It carries genuine downside risk, though — if total exclusion performs
comparably, it undercuts a central design claim. Worth running privately before
deciding whether it belongs in the paper.

## Where these came from

Three throwaway diagnostics motivated this folder and have since been deleted.
Their findings, for the record:

- **Tuning-split resampling.** Selecting `s` on 20 different professor-level
  resamples gave SD 0.23 and a range of 0.23–0.94, clustered into modes around
  0.37, 0.62 and 0.91. The loss surface has several near-equivalent minima.
- **Training-professor tuning.** Tuning `s` on training professors only — the
  arrangement the pipeline now uses — gives 0.83, three grid steps from the
  0.86 originally reported on the full sample.
- **Downstream sensitivity sweep.** Deltas correlate 0.966–0.9995 across the
  modal range with mean divergence under 0.09 rating points, and expert accuracy
  stayed significant at every value tested. `sensitivity_across_s.py` is the
  paper-ready distillation of that sweep.
