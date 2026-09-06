# Paper TODO

## Current state

- The pipeline uses fixed linear attenuation: \(\zeta = 1-D_{\mathrm{misc}}\)
  (`S_VALUE = 1.0`). There is no `s` tuning or grid search.
- The existing manuscript has been updated to remove the obsolete `s`-selection
  narrative. Do not add robustness material to this long-form manuscript; it is
  source material for the LAK draft.
- The permutation control preserves the `D_misc = 0` pattern, so every shuffle
  evaluates the same 77 expert pairs.
- The next blocking input is the remaining expert labels.

## Next work


1. **When all expert labels are available, update validation.**
   - Resolve one consensus label per pair using majority of cast votes; ties are
     unsure and remain incorrect under the existing scoring convention.
   - Keep this rule in one shared function used by validation, robustness, and
     sensitivity analyses.
   - Report overall, coarse, and fine accuracy with 95% Wilson intervals.
   - Report Fleiss' kappa for inter-rater agreement.
   - State the three dropped pairs (77 evaluable of 80) and the treatment of
     unsure labels.

2. **Rerun and archive the final evidence.**
   - Run validation with the multi-expert consensus.
   - Run robustness with 1,000 permutations after the validation update.
   - Save the console output and resulting CSVs; do not cite the older
     `newresults.md` permutation output, which predates the fixed-population
     control.

3. **Write the LAK draft as a new file.** Draw from the existing manuscript and
   add the multi-expert and robustness evidence. Decide the final robustness
   presentation only after the rerun; likely candidates are exponent sensitivity,
   delta--`D_misc` permutation controls, and the fixed-set expert permutation
   result.

## Decisions already made

- Use a fixed, linear attenuation rule rather than selecting an exponent.
- Keep the long-form manuscript coherent and minimal; put new robustness results
  in the LAK version.
- In the permutation control, shuffle positive `D_misc` values only. Zeros stay
  zero, preserving the analytic population and all evaluable expert pairs.
- Do not use expert accuracy at alternative exponents to choose the operating
  exponent; the paired-comparison difficulty changes with adjustment scale.

## Practical notes

- `src/robustness.py` prints summary reports to the console; capture the console output when archiving a run.
- The saved model is used by attenuation and robustness. If the regression model
  is retrained, rerun attenuation, validation, robustness, and affected figures.
- `Paper/worked_examples.py` is the cross-file check for the examples and should
  be run after any change that alters attenuation outputs.
