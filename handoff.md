# Handoff

## Where the project stands

The model and pipeline are working on the corrected 17,127-review corpus. The
attenuation mechanism is fixed and linear:

\[
\zeta = 1-D_{\mathrm{misc}}.
\]

`S_VALUE = 1.0` in `constants.py`; exponent tuning and its grid search were
removed. The existing manuscript now reflects this and is intended to remain a
coherent long-form source document. The next publication deliverable is a new
LAK draft, not a further expansion of the current manuscript.

## Last verified single-expert results

These are the pre-multi-expert reference results from the fixed-linear run:

| Result | Value |
|---|---:|
| Held-out regression MAE / Spearman / R2 | 0.6347 / 0.7352 / 0.6168 |
| Reviews with `D_misc > 0` | 10,375 of 17,127 (60.58%) |
| Held-out miscellaneous reviews | 2,052 |
| Expert accuracy | 62/77 = 80.5% |
| Coarse / fine expert accuracy | 38/43 = 88.4% / 24/34 = 70.6% |
| Delta+ / Delta- Pearson vs `D_misc` | 0.6872 / -0.7077 |

These figures must be rerun after multi-expert consensus is implemented.

## Critical implementation facts

- Expert pairs: 80 labels were supplied; three pairs cannot be matched to the
  adjusted data, leaving 77 evaluable pairs. This is normal don't waste attention on it.
- The permutation control is fixed: it permutes only positive `D_misc` values,
  keeps zeros fixed, and therefore preserves the same expert-pair population in
  every shuffle. Rerun it with 1,000 permutations before using it in the LAK
  paper.
- Multi-expert consensus, confidence intervals, and Fleiss' kappa are not yet
  implemented. They are the immediate next task once all labels arrive.
- The CatBoost model uses fixed 1,000-iteration fits without early stopping.
  

## Next-session checklist

1. Confirm the final expert-label file and column names.
2. Implement shared majority-vote consensus and update validation output.
3. Add Wilson intervals and Fleiss' kappa.
4. Rerun validation and robustness; archive the outputs.
5. Create the LAK manuscript and choose a compact robustness presentation.

## Safe operating notes

- `src/robustness.py` prints summary reports to the console; capture the console output when archiving a run.
- Retraining the model requires rerunning attenuation, validation, robustness,
  and relevant figures.
- Run `Paper/worked_examples.py` after any output-changing pipeline rerun to
  verify the manuscript examples against the generated attenuation data.
- `newresults.md` contains a superseded robustness run from before the
  fixed-population permutation correction; retain it only as an audit trail.
