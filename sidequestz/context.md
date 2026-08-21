# sidequestz

Standalone analyses that sit beside the pipeline. Nothing here modifies it —
every script loads the trained model, never refits, and writes only into
`sidequestz/output/`.

**Most of this folder has moved into the pipeline.** The permutation control and
the s-sensitivity tables are now `src/robustness.py`, stage 7, run with
`python pipeline.py --robustness`. What remains here is genuinely peripheral.

Run from the project root:

```
python sidequestz/worked_examples.py               # paper maintenance
python sidequestz/expert_confidence_intervals.py   # interim; folds into validation.py later
```

On a cp1252 console, prefix with `PYTHONIOENCODING=utf-8` — output containing
`Δ` raises `UnicodeEncodeError` when piped or redirected.

---

## The scripts

### `worked_examples.py` — paper maintenance, not optional

Recomputes the Section 3.9 worked examples (`ex1.tex`, `ex2.tex`, `ex3.tex`) at
the current `S_VALUE` and prints each `s`-dependent quantity beside the value
currently written in the paper, flagged changed or unchanged. Emits paste-ready
LaTeX table bodies to `output/worked_examples.tex`.

Used to move the examples from `s = 0.86` to `0.83`. Rerun it whenever `s`
changes — the examples are hand-traced prose and are the easiest thing in the
paper to leave stale.

Three things to know:

- **`--s` lets you regenerate at any exponent.** Running at 0.86 and diffing
  against the committed `.tex` is how the harness was verified before its 0.83
  output was trusted. Every `s`-independent value reproduced exactly.
- **It doubles as a cross-file consistency check.** It recomputes deltas straight
  from the model and compares them to `attuned_ratings_full.csv`, warning if the
  pipeline's outputs were produced at a different `s`. This guarded the
  `S_VALUE`-vs-tuned-`s` divergence before that bug was fixed; it is still worth
  keeping as a tripwire. It is not wired into `pipeline.py`, so it has to be run
  deliberately.
- **Its Section 1 output is un-anonymized.** Clause text carries real professor
  names where the paper writes `[instructor]`. Do not paste that section into the
  `.tex`. Section 1 is `s`-independent anyway — it is emitted only to confirm
  that clause segmentation and ATC did not shift.

### `expert_confidence_intervals.py` — interim location

Wilson 95% confidence intervals on the Section 4.4 accuracies. `n = 77` after
three pairs drop for missing `review_id`s, which is small enough that a reviewer
will ask; reporting the interval pre-empts the objection.

The intervals will be wide. That is the honest picture, and stating it is better
than having someone else compute it. The claim worth making is that the lower
bound sits above chance — the script prints that check explicitly.

Watch the fine-grained condition. Those are pairs where the two reviews received
nearly the same adjustment, so the model is close to indifferent and accuracy
should be lowest by construction; its interval may well straddle 0.5. That is
the expected shape rather than a failure — accuracy rising with the size of the
separation is evidence that $|\Delta|$ carries graded information — but it needs
to be written up that way rather than presented as an independent success.

Wilson rather than the normal-approximation interval, because the latter
misbehaves at proportions near 1 and at small `n`, both of which apply.

**This is scheduled to move into `src/validation.py`** alongside the majority-vote
label handling, once the two additional expert label sets exist. It lives here
until then so it stays runnable against the single-expert file. See the
"Expert validation" section of `Paper/todo.md`.

---

## Notes

**Expected exposure.** The permutation control and the sensitivity tables are
uniformly favourable — there is no plausible outcome that weakens the paper. The
confidence intervals are favourable in the sense that matters (they pre-empt an
objection) but they will make the fine-grained condition look weaker than the
bare accuracy did, which is the honest picture.

**Deliberately not included: the loss-versus-`s` curve.** The `s` selection
procedure has several near-equivalent local minima, which is why resampling the
tuning set moves the selected value around. Plotting the curve advertises that
directly. Table A of the sensitivity analysis conveys the useful half of the
message — the choice does not matter much downstream — without drawing attention
to the soft spot. This is a presentation judgement, not a correctness one: the
multimodality is real, and if a reviewer asks, the honest answer is that the
objective does not uniquely identify `s` and the sensitivity tables are why that
is acceptable.

**Considered and rejected: an ablation against total exclusion.** Section 3.5
asserts that proportional attenuation is preferable to zeroing out `E_misc`
entirely, and never tests it. Not worth running, for two reasons.

The validation metric is not scale-free. Total exclusion produces larger deltas,
larger deltas produce larger `delta_diff`, and larger `delta_diff` shifts pairs
into the regime where the paired comparison is easy. So the comparison would
partly reward aggressive attenuation for reasons unrelated to measurement
quality, and "total exclusion scores higher" would be close to uninterpretable.

More fundamentally, proportional down-weighting is a measurement-theoretic
commitment following Huber's robust-estimation argument — down-weight
contaminated observations rather than discard them — not a hypothesis to settle
by whichever variant maximises a downstream accuracy number. Validating it that
way would be optimising the wrong objective.

The residual risk is that a reviewer asks "why not just exclude?" anyway. That is
answered in Section 3.5 on principle; the todo carries an item to make the
argument slightly more explicit there.

(For the record: total exclusion is the `s → 0` limit of the existing family,
since `zeta = 1 - D^s` tends to 0 for any `D > 0` as `s` tends to 0. So it could
have been tested for free as an extra row in the sensitivity tables. The decision
not to is about what the test would mean, not about what it would cost.)

## Where these came from

Three throwaway diagnostics motivated this folder and have since been deleted.
Their findings, for the record:

- **Tuning-split resampling.** Selecting `s` on 20 different professor-level
  resamples gave SD 0.23 and a range of 0.23–0.94, clustered into modes around
  0.37, 0.62 and 0.91. The loss surface has several near-equivalent minima.
  These modes are the source of `SENSITIVITY_S_VALUES` in `constants.py`, and
  they were measured against an earlier model — re-derive them after the rerun.
- **Training-professor tuning.** Tuning `s` on training professors only — the
  arrangement the pipeline now uses — gives 0.83, three grid steps from the
  0.86 originally reported on the full sample. The paper has since been moved to
  0.83 throughout; downstream numbers shifted by at most 0.02 rating points.
- **Downstream sensitivity sweep.** Deltas correlate 0.966–0.9995 across the
  modal range with mean divergence under 0.09 rating points, and expert accuracy
  stayed significant at every value tested. Stage 7's sensitivity tables are the
  paper-ready distillation of that sweep.

**Removed:** `find_funny_reviews.py` (conference-slide quote mining; deleted, not
a result). Its outputs are still in `output/` — `funny_reviews.csv`,
`hook_reviews_hook.csv`, `hook_reviews_chaotic.csv` — and now have no generator.
They contain un-anonymized review text. Delete them once the slides are final.
