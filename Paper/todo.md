# Paper TODO — changes required after the codebase fix

The pipeline no longer tunes `s` on the data it reports on. What changed:

- `s` is now selected on **training professors only** (the same professors the
  CatBoost model was fit on), giving **s = 0.83** rather than 0.86.
- Section 4.3 metrics are now computed on **held-out professors** — 206
  professors, 2,052 reviews with miscellaneous content — seen by neither the
  model nor the `s` grid search.
- Section 4.4 (expert validation) still uses the full sample, deliberately.

Everything below follows from that. Regenerating figures, tables and numbers is
assumed and not itemised except where a number's *meaning* changes, not just its
value.

---

## 1. Must change — claims that are no longer accurate

### 1.1 Future Work, line ~1175 — **highest priority**

Currently reads:

> Additionally, future work should evaluate the performance of the attenuation
> mechanism on a held-out dataset. This would address the circularity identified
> in the present research, where the $s$ parameter was optimized on the full
> dataset...

**This is now done.** Leaving it in tells a reviewer you have a known circularity
problem you chose not to fix — directly contradicting the methodology. Delete it
and, if you want something in its place, point at what remains genuinely open:
evaluation on a second dataset, or a formal external criterion.

### 1.2 Limitations, line ~1147

Currently:

> Importantly, the $s$ parameter was optimized on the full dataset, which
> overestimates the generalizability of reported correlation improvements.

No longer true. Replace with the limitation that *does* survive — that the
selection procedure does not uniquely identify `s`:

> The selection procedure for $s$ does not identify a unique optimum; several
> values in the search range produce near-equivalent loss. Resampling the tuning
> professors selects values ranging from 0.23 to 0.94. Downstream adjustments are
> highly stable across this range (Pearson $r > 0.96$ between $\Delta$ vectors),
> so the reported results do not depend materially on the selected value, but the
> exponent itself should be treated as weakly identified.

This is a genuine limitation and stating it plainly is stronger than having a
reviewer infer it. It also sets up the sensitivity tables if you include them.

### 1.3 Section 3, line ~566 — the `s` sentence

Currently:

> The value of $s = 0.86$ that maximizes these criteria is chosen for all
> subsequent stages of the framework.

Two problems: the value is now 0.83, and "maximizes these criteria" implies a
unique optimum that does not exist. It is not flatly false — the grid search does
return the argmin — but it overclaims. Suggested:

> The grid search selects $s = 0.83$, which is used for all subsequent stages of
> the framework. Selection is performed using only reviews from the training
> professors, so that the correlation improvements reported in Section 4.3 are
> measured on professors excluded from both model fitting and parameter
> selection.

That sentence does double duty — it fixes the overclaim and states the
non-circularity in the place a reviewer looks for it.

### 1.4 "Stratified" is the wrong word — lines ~519, 543, 741, 765, 1002

The paper repeatedly says "professor-level **stratified** split" and "GroupKFold
**stratified** by professor ID". The split is **grouped**, not stratified.

- *Grouping* keeps all rows of a unit on one side of the split. This is what
  `GroupKFold` and your `prof_ID`-based split do.
- *Stratification* preserves the class distribution across splits. You are not
  doing this.

Reviewers who know the distinction will read it as either sloppiness or a
misunderstanding of your own leakage control — which is a shame, because the
control itself is correct and is a genuine strength. Replace every instance with
"professor-level grouped split" / "grouped 5-fold cross-validation (GroupKFold,
grouped by professor ID)".

---

## 2. Should add — states the fix where reviewers look

### 2.1 Make the three-way data usage explicit (Section 3, near line 519)

Add a short paragraph stating that the professor-level split governs three
stages, not just model training:

> An 80–20 professor-level grouped split is applied once and reused throughout:
> the CatBoost regressor is trained on the training professors, the attenuation
> exponent $s$ is selected on those same professors, and all attenuation
> validation metrics in Section 4.3 are computed exclusively on the held-out
> professors. No professor contributes reviews to both parameter selection and
> reported evaluation.

That last sentence is the one that answers the circularity objection outright.
Worth stating in exactly that form.

### 2.2 Section 4.3 header — say what population the metrics describe

State up front that Section 4.3 reports on held-out professors, with the n
(206 professors / 2,052 misc reviews). Otherwise a reader comparing against the
10,380 in Section 5 will assume an error.

### 2.3 Section 4.4 — justify the different sample

Expert validation still uses the full sample. This is defensible, but say why
rather than leaving the inconsistency unexplained:

> Expert validation is reported on the full sample. The paired comparisons were
> drawn across all professors, and restricting them to held-out professors would
> leave too few pairs for meaningful inference. Circularity is not a concern
> here: expert judgements are made from review text alone and enter no objective
> used in fitting.

### 2.4 Reframe Section 4.3's rhetorical weight

Sections 4.3.2 and 4.3.3 measure quantities the `s` loss is built from. The
held-out split now makes them legitimate evidence rather than a restatement of
the objective — but they are still *verification that the mechanism behaves as
specified*, whereas Section 4.4 is the evidence that the behaviour corresponds to
something real. A sentence in the Section 4.3 intro framing it that way costs
nothing and pre-empts the sharper version of the objection.

---

## 3. Numbers to regenerate

Run the pipeline, then `--visualize-only`. Section 4.3 figures are now held-out
only, so they must be regenerated, not merely re-checked.

- **Section 3.9 worked examples** (Tables `tabex1`–`tabex3`) — traced at s = 0.86;
  every $\zeta$, weighted emotion and $\Delta$ needs recomputing at 0.83. Easy to
  overlook because they read as prose.
- **Section 4.3.1** — SHAP figures (`SHAPdelta_importance`, `SHAPpct_change_shap`),
  now computed on held-out professors.
- **Section 4.3.2** — both correlation figures.
- **Section 4.3.3** — Table `tabcorrelation_deltas`, the `att-vs-misc` scatter,
  and the Mann-Whitney statistics (U, p, rank-biserial, and both bin sizes).
- **Section 4.4** — Table `tabexternal-validation`; bin membership shifts slightly
  with `s`, so pair counts may move even where accuracy does not.
- **Section 5.4** — Table `tabadjustment-stats` and surrounding prose. Latest run:
  60.59% attuned, mean $|\Delta|$ 0.2072 (paper currently says 0.2047), max
  $|\Delta|$ 2.6068. Very close to the existing values.
- **Section 6** — line ~1104 repeats 0.2047; update alongside 5.4.
- **Abstract and Conclusion** — check for any quoted figure.

Sanity check: at s = 0.83 versus 0.86 the deltas correlate above 0.999, so
anything that moves by more than a rounding step is worth investigating rather
than transcribing.

---

## 4. Optional additions

See `sidequestz/context.md`. Sensitivity tables, Wilson confidence intervals on
the Section 4.4 accuracies, and a permutation control. All optional; the
permutation test is the highest-value one if space allows.

If the sensitivity tables go in, they pair naturally with the rewritten
limitation in 1.2 — the limitation states `s` is weakly identified, the tables
show it does not matter.

---

## 5. Ordering suggestion

1. Item 1.1 (delete the Future Work paragraph) — takes a minute, and leaving it
   in actively contradicts the rest of the paper.
2. Items 1.3, 1.4, 2.1 — the wording changes, before regenerating anything.
3. Regenerate figures and numbers (Section 3).
4. Item 1.2 and the Section 2 additions once the new numbers are in hand.
5. Decide on `sidequestz` extras last, based on remaining space.
