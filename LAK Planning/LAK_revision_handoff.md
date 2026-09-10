# LAK manuscript revision handoff

Updated 9 September 2026. This records the current manuscript state and only the remaining revision work.

## Current paper position

The paper is a proof of concept for examining a fitted rating model. It characterizes learned relationships between topic-specific emotion features and ratings, then traces how predicted ratings respond when taxonomy-excluded affect is attenuated. It does not establish that adjusted ratings measure teaching quality better than raw ratings, nor that attenuation outperforms density alone on the expert-ranking task.

## Completed

- Reframed the paper from correction to taxonomy-sensitivity and model-response analysis. “Taxonomy-excluded affect” is the canonical term.
- Aligned the research questions, contributions, method, discussion, conclusion, and robustness reporting with that framing.
- Documented transformed-input interpretation, descriptor aggregation, TreeSHAP computation, the $D=1$ collapse, the adjustment tail, and pair-construction limitations.
- Updated expert comparison to test alignment between fitted-model response magnitude and expert judgments of validity and/or topical relevance, without implying that experts applied the study taxonomy.
- Corrected permutation and bootstrap interpretation.
- Added the expert-validation instructor metadata line. `expert_pair_instructor_metadata.py` at the project root reproduces the calculation.
- Added the tau development-set overlap statement. `tau_validation_id_overlap.py` at the project root reproduces the review-ID and clause-overlap check.
- Added clustered-data scope language for the Wilcoxon and Mann--Whitney tests.
- Reworked the discordant-pair table for readability: it now separates decision signals from full anonymized review text, compares one attenuation-only and one density-only success, and uses the available table width.
-Inspect the six discordant expert pairs: the three attenuation-only and three density-only successes. Classify each divergence as affect--density decoupling, weak model response, upstream misclassification, or no discernible basis. Also inspect the three unanimous expert disagreements. Report a pattern only if the small set supports one. (Tentatively done)
## Remaining work


1. Write the concise paragraph on what attenuation adds beyond $D_{misc}$. Retain the observed lack of aggregate expert-ranking advantage while explaining the distinct analytic outputs: learned feature--rating relationships and the fitted model’s signed response to attenuation. Use the pair inspection only if it provides defensible evidence.

2. Finalize the title. Retain a taxonomy-sensitivity signal, remove “Affective Noise,” and retain validity-weighted attenuation as the method name. Define the weights as content proportions, not validity coefficients.

3. Write the abstract last. Include the mechanism and boundary, 17,127 reviews, grouped evaluation, and 83.1% agreement on 77 pairs with the density-only result adjacent. Include coarse/fine results only if space permits. Do not claim validity improvement, uniform conservatism, or an attenuation advantage over density.

## Wording to preserve

- “Taxonomy-excluded” is an operational category under a stated taxonomy, not a finding of irrelevance.
- $\Delta$ is the fitted model’s response to feature scaling with other inputs fixed, not a causal estimate of contamination.
- The density-only result shows no observed aggregate expert-ranking advantage on the sampled pairs; it does not make the predictive model redundant for studying learned relationships or attenuation response.
- The review queue is a workflow hypothesis, not an evaluated intervention.
