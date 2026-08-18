# Paper TODO

## Methodology and reproducibility

1. **Rerun the full pipeline after the missing-record preprocessing fix.** The
   five blank and unrated records are now excluded, producing an expected
   analytic corpus of 17,127 reviews. Regenerate all processed data, model
   outputs, validation results, and dependent figures before revising results.

2. **Create a professor-level train/CV/test design.** Reserve the final test
   professors before model selection; use only the remaining development
   professors for grouped cross-validation and CatBoost early stopping. The
   final test set must not be used to select the stopping iteration.

3. **Rerun the full pipeline after the split change.** Regenerate the trained
   CatBoost model, feature importance, attenuation outputs, validation metrics,
   and all dependent figures and tables.

4. **Update reported results and wording.** Replace the current final-model
   metrics and every downstream result affected by the rerun. Describe the
   resulting final test set as untouched only after the new design is in place.

## Optional analyses

5. Run the optional analyses in `sidequestz/`: sensitivity tables, Wilson
   confidence intervals, and the permutation control (highest priority). See
   `sidequestz/context.md`.

6. Add explicit “full sample” labels to the external-validation and
   adjustment-outcomes tables for population-label consistency.
