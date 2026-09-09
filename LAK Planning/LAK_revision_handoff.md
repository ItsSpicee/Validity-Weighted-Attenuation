# LAK manuscript revision handoff

Updated 8 September 2026. This handoff records the currently saved manuscript and the next revisions to consider. It does not claim that unverified analyses have been run.

## Current paper position

The paper should be presented as a proof of concept for examining a fitted rating model: it characterizes learned relationships between topic-specific emotion features and ratings, then traces how predicted ratings respond when taxonomy-excluded emotion features are attenuated. The paper does not establish that adjusted ratings measure teaching quality better than raw ratings, nor that attenuation outperforms density alone for the selected expert-ranking task.

## Completed in this revision session

- Removed an unsupported explanation for the exponent-sensitivity pattern; results now describe the observed sensitivity only.
- Replaced references to emotion "intensity" with model-estimated emotion-label probabilities or emotion features.
- Removed two forced Marsh and Roche attributions that appeared to justify the proportional attenuation rule.
- Clarified that the full mechanism's distinct contribution beyond density is examination of learned feature--rating relationships and of the model's signed response to attenuation.
- Updated the expert-comparison method: it now tests whether the magnitude of the fitted model's response aligns with expert judgments of validity and/or topical relevance. It no longer implies that experts applied the study taxonomy.
- Aligned discussion and conclusion: model analysis is an established analytic output; stakeholder benefit from presenting those outputs remains unevaluated.

## Remaining changes, in recommended order

1. **Title and abstract.** Both remain unfinished or misaligned. Use a title that signals taxonomy-based model sensitivity rather than validated weighting or identified "noise." The abstract should name the 17,127-review RMP proof of concept, grouped evaluation, expert comparison, 83.1% agreement on 77 pairs, and the density-only match. State the model-analysis contribution positively and avoid claiming teaching-quality correction.

2. **Clarify transformed-input interpretation.** In Method or Results, add that attenuation creates counterfactual feature vectors for the fitted model. The $D_{\text{misc}}=1$ case zeros all miscellaneous emotion features and produces the common attenuated prediction of 3.65. This is a property of the representation and fitted model, not an empirically validated neutral-rating target. Keep the existing report that 9.6% of adjusted values fall outside the 1--5 scale.

3. **Report aspect-term categorization reproducibly.** State the size and separation of the manually inspected threshold-development set, including whether it overlaps the 386-clause evaluation set. Specify exactly how multiple descriptor embeddings are combined into each category representation. Verify that the claimed validation procedure is accurately described.

4. **Strengthen the density comparison with existing cases.** Inspect the six pairs where attenuation and density have exclusive successes, plus the three unanimous expert/model disagreements. Report a small qualitative diagnostic if the cases yield a clear pattern; otherwise state that they do not. This is the best existing-data route to explain what the rating model adds beyond density.

5. **Tighten statistical reporting.** Define SHAP importance calculation, normalization, and reference/background data. Treat review-level Wilcoxon and Mann--Whitney results cautiously because reviews are clustered within instructors; emphasize effect sizes and descriptive patterns. Keep permutation results conditional on shuffling density both as a model feature and attenuation input.

6. **Complete expert-study reporting.** Document the precise expert prompt, screening/replacement steps during pair construction, number of distinct instructors, and any instructor recurrence across pairs. Retain the scope boundary: this study tests alignment of an ordering with expert review judgments; it does not validate adjustment direction, magnitude, or teaching-quality measurement.

7. **Refine the worked example.** Explicitly state that categorizing interpersonal conduct as Miscellaneous and subject knowledge as Instructional Effectiveness are contestable model assignments. Explain that the example is intended to expose those decisions for inspection, not establish their correctness.

8. **Resolve access and end matter.** Replace the generic public-code statement with a double-blind-accessible route and accurate disclosure of code, expert instructions, pair membership, labels, density values, deltas, and restrictions on review text. Complete funding and verify the ethics statement.

9. **Reduce and compile.** The latest saved PDF was 16 pages before the current edits and before the abstract was finished. LAK27 full papers permit 10--14 pages including references and notes for practice. Consolidate repeated gap statements, repeated numerical discussion, and overlapping limitation/non-use prose; then compile and inspect the current PDF.

## Wording to preserve

- "taxonomy-excluded" is an operational category under a stated taxonomy. It is not a finding that a clause is irrelevant or that its affect is invalid.
- $\Delta$ is the fitted model's response to feature scaling, with other inputs fixed. It is not a causal estimate of contamination in a raw rating.
- The density-only result demonstrates no aggregate expert-ranking advantage for attenuation on the sampled pairs. It does not make the predictive model redundant for studying learned feature--rating relationships or its response to attenuation.
- The proposed review queue is a workflow hypothesis, not an evaluated decision-support intervention.
