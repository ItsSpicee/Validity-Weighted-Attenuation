# New expert and robustness interpretation/framing

Master plan for the LAK27 manuscript — 6 September 2026

## 1. Strategic decision

Build the paper around a theoretically motivated, auditable method whose evaluation distinguishes supported behaviour from unresolved discrimination. The expanded evaluation is the empirical foundation of that contribution. It establishes what the mechanism does reliably in this study and where stronger interpretation is unwarranted.

**Recommended central claim**

> Validity-weighted attenuation makes a stated relevance assumption computationally explicit and traceable. In this proof of concept, its relative adjustments align strongly with expert judgments on large adjustment contrasts and exhibit stable aggregate patterns, while fine-grained superiority over shuffled density assignments remains unestablished under two binning specifications.

The acceptance strategy is to make the contribution substantial, its educational purpose concrete, and its claims easy to audit. Transparent reporting improves the credibility of those claims; a nonsignificant result does not by itself increase acceptance prospects. No acceptance probability can be inferred from these analyses.

The paper should remain a conceptual and technical proof of concept with bounded empirical evidence. Its value should survive removal of every significance label: a motivated operation, an inspectable representation, and an informative evaluation of its capabilities and limits.

## 2. Evidence base and status

The numerical source of truth is [expert_and_robustness_results.md](expert_and_robustness_results.md). The implementations are [validation.py](../src/validation.py), [robustness.py](../src/robustness.py), and [attenuation.py](../src/attenuation.py). The target manuscript is [LAK_draft/main.tex](LAK_draft/main.tex).

This plan supersedes the old single-expert and fine-discrimination interpretations in the existing framing documents. It is a plan and wording bank; it does not itself edit the manuscript.

### Expert evidence at the operating point

| Comparison | Majority agreement | 95% Wilson CI | Three-category Fleiss' κ |
|---|---:|---:|---:|
| Overall | 64/77 = 83.1% | 73.2–89.9% | .658 |
| Coarse | 43/43 = 100% | 91.8–100% | .819 |
| Fine | 21/34 = 61.8% | 45.0–76.1% | .469 |

Coarse means a difference of at least 0.5 between the reviews' absolute attenuation deltas; fine means a difference in [0, 0.5). These are **model adjustment contrasts**, not independent measurements of differences in validity or off-topic content.

There are no missing votes or absent majorities among the 77 retained pairs. One majority is non-directional and counts as incorrect under the specified directional scoring rule. Use the actual response meaning, “both valid,” rather than silently relabelling it “unsure.” Confirm the original annotation instructions when writing the protocol.

### Permutation evidence

| Outcome | Observed | Recomputed-bin null mean | Recomputed-bin p | Fixed-bin null mean | Fixed-bin p |
|---|---:|---:|---:|---:|---:|
| Overall majority agreement | .8312 | .6330 | .0010 | Same overall population | Same result |
| Coarse majority agreement | 1.0000 | .8491 | .1798 | .6887 | .0010 |
| Fine majority agreement | .6176 | .5988 | .3776 | .5625 | .3207 |

| Recomputed group | Observed n | Permutation mean n | SD | Range |
|---|---:|---:|---:|---:|
| Overall | 77 | 77.00 | 0.00 | 77–77 |
| Coarse | 43 | 10.51 | 2.85 | 3–20 |
| Fine | 34 | 66.49 | 2.85 | 57–74 |

All 1,000 shuffles produced nonempty subgroups. Fixed groups retain 43 coarse and 34 fine pairs. The two specifications use the same shuffles and predictions; they are related analyses, not independent replications.

### Other robustness evidence

| Evidence | Result | Supported interpretation |
|---|---|---|
| Most distant exponents, s=.5 versus 1.5 | Pearson r=.9635; Spearman ρ=.6887; mean absolute delta difference=.0830; maximum=1.1482 | Aggregate linear correspondence is high; ordering and some individual adjustments are more sensitive. |
| Expert sensitivity, groups fixed at s=1 | Overall 83.1–88.3%; coarse 100% throughout; fine 61.8–73.5% | The coarse result persists across tested exponents; close comparisons vary by up to four correct decisions out of 34. |
| Positive delta versus true density | Observed r=.6872; shuffled mean=.2327; p=.0010 | The original density assignment produces a stronger internal relationship under this perturbation. |
| Negative delta versus true density | Observed r=−.7077; shuffled mean=−.1579; p=.0010 | The corresponding negative relationship is stronger in magnitude under the original assignment. |
| Professor bootstrap, Pearson correlations | Positive 95% CI [.6514, .7202]; negative [−.7406, −.6715] | Internal relationships are stable under resampling of the held-out professors, conditional on the fitted model. |
| Professor bootstrap, Spearman correlations | Positive 95% CI [.5569, .6610]; negative [−.6493, −.5498] | The corresponding rank relationships persist under the same resampling scheme. |

The bootstrap does not resample experts, refit the model, or establish external criterion validity. The expert comparison sample and the held-out robustness sample must remain clearly distinguished.

## 3. The evidence argument that should organize the paper

### Layer A: Educational and conceptual purpose

Open-ended teaching feedback contains multiple kinds of evidence and student experience. Any operation that changes how this content contributes to a numerical summary makes a relevance judgment. The method's conceptual contribution is to state that judgment explicitly, implement it proportionally, and preserve the material needed to inspect and contest it.

Use “content classified outside the stated pedagogical taxonomy” where precision matters. A taxonomy may omit meaningful educational concerns. Classification outside it does not establish that a student's experience is unimportant or that its affect is measurement error.

### Layer B: Mechanistic behaviour

Show how the fixed rule changes model inputs and produces review-level deltas. Treat density–delta relationships and attribution shifts as internal evidence about the implemented operation. These checks matter, but are not independent confirmation that adjusted scores better represent teaching quality.

### Layer C: Human-judgment evidence

The three-expert panel supplies a distinct source of evidence about relative review judgments. Report high coarse agreement and weaker fine agreement together. The main contribution of adding experts is a less individual-dependent assessment and visibility into disagreement, rather than a guaranteed increase in accuracy.

Do not present majority voting as eliminating subjectivity. Do not describe the change from the old single-expert score as deterioration of the model: the criterion changed, and the operating-point model is being evaluated against a different reference.

### Layer D: Perturbation and limits

The permutation analyses distinguish two questions. The exponent and bootstrap analyses distinguish stability of aggregate relationships from sensitivity of individual comparisons. Together they make the evaluation informative enough to support bounded interpretation, rather than a collection of favourable diagnostics.

The resulting answer to RQ3 is mixed and specific: aggregate coherence is stable under the tested perturbations; expert alignment depends on the comparison condition; fine-grained superiority is unestablished under both permutation specifications.

## 4. How to interpret both permutation analyses

### Preserve the original recomputed-bin test

Its statistic includes group assignment: recompute deltas, predictions, and bin membership under each shuffled density assignment. Changing the denominator is not itself a coding error or an invalid permutation statistic.

It asks whether agreement among pairs classified as coarse or fine by the original pipeline is unusually high relative to agreement within the corresponding groups produced by shuffled pipelines.

### Describe the fixed-bin analysis as supplementary

It keeps the original evaluable pairs and operating-point group assignments fixed while recomputing predictions. It asks how agreement on those particular groups behaves under shuffled assignments. It was added after examining the first analysis and should be identified as a supplementary sensitivity analysis, not retrospectively called a pre-specified primary test.

Its strong coarse result supports the descriptive finding that shuffling degrades agreement on the original coarse set. Neither the fixed-bin nor recomputed-bin analysis isolates the incremental benefit of the proportional rule over all simpler alternatives.

### Explain the coarse divergence without over-attributing it

Under recomputation, coarse membership contracts from 43 to a mean of 10.51 pairs. The resulting selected groups have a high null mean agreement (.8491), and 179 of 1,000 reach perfect agreement. With fixed membership, the null mean is .6887 and none reaches the observed value.

The difference involves **both group size and group composition**. The evidence is consistent with the smaller selected groups making perfect agreement easier to obtain. These summaries do not quantify how much of the p-value difference is caused by sample size alone. Avoid “the coarse test fails simply because there are fewer pairs.”

### State the fine finding accurately

> We cannot reject the respective fine-grained permutation null under either binning specification.

This is consistency across analysis choices, not proof of the null, evidence of equivalence, or two independent confirmations. The observed advantage is 1.9 percentage points over the recomputed-bin null mean and 5.5 points over the fixed-bin mean; uncertainty remains substantial.

### Bound what the shuffle tests

The control shuffles positive density values while preserving zeros and the overall analytic population. It changes density wherever consumed, including the model feature and attenuation factor; it holds the fitted model and other features fixed. Correlations are evaluated against the original densities.

Interpret it as a specified density-assignment perturbation. Exact inferential claims additionally depend on the null's exchangeability assumptions. Density is related to other model features, and pair selection used original model outputs; neither binning choice automatically resolves those dependencies or selection issues. Explain the scheme and keep the conclusion conditional, rather than claiming the shuffle proves the relevance proxy correct. This qualification applies to the overall test as well as the subgroups.

Retain the one-sided Monte Carlo calculation (hits+1)/(1000+1). With zero hits, report p=.001, not p<.001. Present the examined outcomes together; do not select a primary outcome after inspecting significance.

## 5. Main-paper presentation and page budget

**Preferred layout:** two compact tables, one short robustness paragraph, and one integrated discussion paragraph.

### Table 1: Expert comparison

Use the three-row expert table in Section 2: n/correct, majority agreement, Wilson interval, and all-response κ. State the response/scoring convention in the caption or immediately preceding protocol. Keep individual-expert rows and κ excluding label-3 votes in supporting material.

### Table 2: Permutation control

Use the compact two-specification comparison from Section 2. Include overall once and both subgroup results. Put the group-size shift in the table note: coarse n=43 observed, mean 10.51 under recomputation; fine n=34 observed, mean 66.49. Put full ranges, SDs, and size diagnostics in supporting material.

If necessary, include the two correlation outcomes as additional rows with a single null result, explicitly marked as independent of expert binning. Do not duplicate identical overall or correlation results under both specifications.

### Compress the existing sensitivity material

The current ten-row pairwise exponent matrix occupies space that is more valuable for the expert findings. Retain a representative adjacent comparison, the extreme comparison including both r and ρ, and the expert accuracy ranges. Move the exhaustive matrix to supporting material. Summarize bootstrap intervals in prose or a compact companion table.

**Fallback if space is exceptionally tight:** report the original overall/coarse/fine test in the main table and add one sentence stating the supplementary fixed-bin coarse and fine results. Both interpretations must remain visible in the main paper; the reader should not need the supplement to discover that coarse conclusions depend on grouping.

The full-paper limit is 10–14 JLA-format pages including references and practitioner notes. The official guidelines also discuss supplemental material; check their current submission instructions when packaging it. [LAK27 submission guidelines](https://www.solaresearch.org/events/lak/lak27/submission-guidelines/)

## 6. Manuscript revision map

| Location | Required change | Purpose |
|---|---|---|
| Title | Consider “Validity-Weighted Attenuation in Teaching-Feedback Analytics: An Auditable Framework and Expert Evaluation.” | Centre the operation and evaluation; avoid requiring readers to accept that all targeted affect is already established noise. |
| Abstract | Replace expert placeholders and fine-significance claim; include 83.1% overall, coarse/fine contrast, and unresolved fine discrimination. | Make the actual empirical contribution clear immediately. |
| Introduction | Present the problem as making relevance assumptions explicit in interpretation of teaching feedback. | Connect the technical operation to an educational need. |
| Contributions | Specify conceptual design, auditable implementation, and a multi-part evaluation that identifies limits. | Give reviewers three assessable contributions. |
| RQ2 | Prefer “How does attenuation change the modelled contribution of affect under the stated taxonomy?” | Match the question to internal rather than external validity evidence. |
| RQ3 | Prefer “How stable are these changes under perturbation, and how does agreement with expert judgments vary across adjustment contrasts?” | Permit a mixed answer without embedding a successful outcome in the question. |
| Expert methods/results | Insert panel description, task, construction, selection, blinding, scoring, denominators, and Table 1. | Make the curated evaluation reproducible. |
| Permutation methods/results | Define the original statistic and supplementary fixed-bin statistic; replace old table and interpretation. | Explain the coarse divergence and fine consistency. |
| Sensitivity | Keep groups fixed at s=1; report stable aggregate patterns and finer decision sensitivity separately. | Avoid a blanket robustness claim. |
| Bootstrap | Replace old numerical intervals; identify the resampling unit and conditional scope. | Prevent conflation with expert uncertainty. |
| Discussion RQ3 | Replace the fine “tiebreaker” and coarse “only a manipulation check” account. | Integrate the new evidence into the argument. |
| Practical implications | Describe an auditable inspection workflow as a proposed use; avoid validated priority or validity rankings. | Establish a meaningful LA connection without inventing an impact study. |
| Limitations | Replace single-expert limitation with panel, sample, selection, taxonomy, and criterion limits. | Explain what remains unresolved after expansion. |
| Conclusion/practitioner notes | Include the fine-grained boundary alongside the contribution. | Ensure the takeaway matches the results. |

Research-question wording can be revised for clarity, but must not imply preregistration or erase the actual analysis chronology.

## 7. Wording bank

### Abstract results passage

> Across 77 curated review pairs, attenuation rankings agreed with a three-expert majority on 83.1% of comparisons, with higher agreement for large adjustment contrasts (100%) than for small contrasts (61.8%). Overall agreement exceeded the shuffled-density benchmark, while neither of two binning specifications rejected the fine-grained permutation null. Aggregate adjustment patterns remained similar across the tested exponents and held-out-professor resamples. These findings support initial method evidence for auditable interpretation of teaching feedback while leaving fine-grained validity ordering unestablished.

### Expert results

> At s=1, model rankings agreed with the expert majority on 64 of 77 pairs (83.1%; 95% Wilson CI [73.2%, 89.9%]). Agreement was 43/43 for coarse pairs (100%; [91.8%, 100%]) and 21/34 for fine pairs (61.8%; [45.0%, 76.1%]). Inter-expert agreement was also lower in the fine condition (Fleiss' κ=.469) than in the coarse condition (κ=.819). The comparison therefore supports stronger alignment on large model adjustment contrasts, with greater uncertainty and disagreement on close comparisons.

### Permutation results

> With bins recomputed after each shuffle, overall agreement exceeded the permutation benchmark (83.1% versus a null mean of 63.3%; p=.001), whereas coarse and fine agreement did not (p=.180 and .378). Recomputed coarse groups contained a mean of 10.51 pairs, compared with 43 observed, and retained a high null mean agreement of 84.9%. A supplementary analysis holding original group membership fixed yielded a coarse null mean of 68.9% (p=.001) and a fine null mean of 56.3% (p=.321). Thus, the coarse comparison depended on whether grouping was recomputed, while neither specification rejected its fine-grained null.

### Discussion synthesis

> The expanded evaluation distinguishes stability of the implemented operation from evidence supporting its interpretation. Aggregate adjustment relationships persisted under the tested perturbations, and large adjustment contrasts aligned strongly with the expert panel in the curated task. Fine-grained agreement was lower, and neither permutation specification established superiority over shuffled assignments in that condition. These findings bound the interpretation of attenuation magnitude: it provides an inspectable model-based signal, while small differences should not be treated as established differences in review validity.

### Practitioner-facing implication

> An adjustment can identify a model response worth inspecting. The original feedback, its clause assignments, and the adjustment trail should be read together. Small differences in adjustment magnitude have not been validated as an ordering of pedagogical relevance.

### Contribution statement

> The study contributes an explicit attenuation rule, a review-level audit trail connecting model adjustments to classified content, and an evaluation combining expert comparisons with perturbation analyses to characterize both supported behaviour and unresolved discrimination.

## 8. Make the fine-grained result scientifically informative

The strongest next addition is a bounded diagnostic analysis of the 13 fine-condition disagreements. An earlier read-only audit of saved labels and deltas found:

| Fine voting pattern | Model agrees with majority | Model disagrees |
|---|---:|---:|
| Unanimous | 16 | 3 |
| Split | 5 | 10 |

This table is an auxiliary audit, not currently part of the primary results report. Reproduce and archive it before inserting it into the manuscript, particularly if any labels or deltas have changed.

Ten of thirteen errors occur on split-vote pairs, but three occur despite unanimity. Examine all thirteen rather than selecting only the most convenient example. Give particular attention to the unanimous failures because panel disagreement cannot explain those cases.

For each case, record the raw pair, votes, model prediction, absolute deltas, measured densities, clause assignments, and any existing annotator notes. Assess possible explanations such as taxonomy coverage, density failing to represent informational relevance, or the relationship between relevance judgments and model adjustment magnitude. Label these interpretations as post hoc and avoid attributing motives or reasoning to experts without their notes.

A compact worked example can show a failure, its visible audit trail, and what remains unresolved. That demonstrates the methodological value of inspectability without claiming that inspectability corrected the error.

Do not use the unanimous subset as the replacement headline evaluation. Do not infer a human reliability ceiling from κ or claim ambiguity caused model failures.

## 9. Anticipate the substantive reviewer objections

| Likely objection | Best response in the manuscript | Evidence limit to retain |
|---|---|---|
| “This is another NLP pipeline with a hand-built weight.” | Explain the specific relevance assumption, why proportional attenuation is a defensible design choice, and how the audit trail exposes its consequences. | The rule is a proposed operationalization, not a psychometric theorem. |
| “Density–delta correlation is built into the method.” | Identify it as internal coherence and separate it from expert evidence. | Shuffling does not validate the taxonomy or proxy. |
| “Fine-grained performance is weak.” | Report it prominently and show consistency across specifications, sensitivity ranges, and diagnostic cases. | No claim of equivalence or demonstrated fine-grained superiority. |
| “Coarse cases were selected to be easy.” | Describe pair construction and model-gap thresholds; report the original and fixed-bin controls together. | Curated agreement is conditional on the selected cases. |
| “The significant fixed-bin result was chosen after the fact.” | Identify its supplementary status and retain the original result in the main text. | It is not an independent confirmatory replication. |
| “A simpler density ranking could do this.” | If feasible, add a transparent benchmark using lower density as the predicted more-valid review, with an explicit tie rule and identical pairs. | Until tested, make no superiority claim over density-only ranking or uniform attenuation. |
| “Expert agreement validates adjusted teaching scores.” | Define the task as relative review judgment, not rating calibration. | No external criterion validates adjustment magnitude or teaching-quality inference. |
| “This is academic analytics rather than learning analytics.” | Ground the problem in interpretation of pedagogical feedback and educator reflection; show how a review trace can be inspected. | Institutional ranking and management use are not the central contribution. |
| “There is no demonstrated stakeholder impact.” | Position the contribution as method development with a concrete proposed workflow. | Do not imply measured benefits to reflection, agency, fairness, or learning. |

The LAK call explicitly includes conceptual development and proof-of-concept work, while asking for meaningful connections to learners, educators, and learning processes. The practical interpretation pathway should therefore be substantive, not a final-paragraph mention of stakeholders. [LAK27 general call, local copy](callforpapers.md)

## 10. Psychometric and protocol precision

Address these in a short methods paragraph and claim-matched limitations, rather than an extensive defensive checklist in the paper:

- Validity concerns the support for an interpretation and use. A relevance taxonomy is part of the argument, not an established ground-truth partition of valid and invalid student experience.
- Explain s=1 through the direct proportional-retention design choice. Huber's robust-estimation principle may motivate downweighting; it does not derive this particular word-density exponent. Classical reliability theory does not make density a measured reliability coefficient.
- Three-expert attenuation validation does not turn the separate, single-expert ATC validation into a three-expert study. Keep these evaluations distinct.
- Report 80 originally annotated pairs and 77 evaluable pairs, with the three unavailable-delta exclusions stated once. Do not infer “no exclusions” from a report based on already-filtered CSVs.
- Describe expert background, independent labelling, blinding, displayed-order randomization, recruitment, instructions, and ATC verification only to the extent documented. Missing procedural facts must be confirmed before drafting factual assertions.
- Wilson intervals condition on these three experts and assume independent pairs. The earlier audit found 154 distinct reviews, but distinct reviews may still share instructors. Check instructor clustering before implying independence is established.
- The earlier audit found 115 of those reviews on the training side and 39 held out. Recheck before reporting those counts; the expert comparison is not wholly out-of-sample. Blinding prevents exposure to predictions but does not make the selected data independent of model development.
- All-response κ is primary. κ excluding label-3 votes is a sensitivity analysis on retained directional responses, not a cleaner estimate of the same response process.
- Maintain the established exponent and scoring rules. Further choices based on this expert panel would be development decisions and require new independent evaluation for confirmatory claims.

For statistical language, distinguish non-rejection from evidence of no effect and report effect magnitudes alongside p-values. [ASA statement on p-values](https://doi.org/10.1080/00031305.2016.1154108)

## 11. Prioritized execution plan

### Priority 0 — Make every existing claim consistent

1. Freeze the updated numerical report and record model, label, code, seed, and parameter versions.
2. Replace the abstract, expert table placeholder, permutation table, and RQ3 discussion together. These are one coordinated revision.
3. Remove old fine p=.007 and coarse p=.233 claims, obsolete single-expert headline values, and the statement that fine discrimination specifically depends on true density.
4. Replace p<.001 with p=.001 wherever it refers to zero exceedances in these 1,000 permutations.
5. Preserve fixed groups in exponent sensitivity and name the supplementary fixed-bin permutation analysis distinctly.
6. Replace blanket exponent robustness with the aggregate-versus-close-comparison distinction.

Completion criterion: a reader can follow every abstract and conclusion claim to a current result without encountering a contradictory passage.

### Priority 1 — Strengthen the educational and methodological contribution

1. Tighten the central claim, contributions, and research questions using Sections 1, 3, and 6.
2. Insert a concise, complete expert protocol and explain the two permutation statistics.
3. Reproduce the fine-disagreement audit; inspect the three unanimous failures and remaining split-vote errors.
4. Use one representative audit-trail example to connect the method to interpretation of pedagogical feedback.
5. Distinguish implemented inspectability from a proposed stakeholder workflow and future impact evaluation.

Completion criterion: reviewers can explain why the contribution matters for teaching-feedback interpretation even after acknowledging that fine discrimination is unresolved.

### Priority 2 — Add evidence only where it addresses a real objection

Consider the density-only benchmark if readily computable on identical pairs. Declare it exploratory, specify tie handling before scoring, and report all conditions. A disappointing baseline comparison is informative and must not be suppressed.

If instructor overlap is substantial, consider a cluster-aware uncertainty analysis suited to the pair structure; do not assume an ordinary row bootstrap fixes shared-instructor dependence.

Do not spend the remaining effort searching for an exponent, subgroup, response exclusion, or threshold that makes fine p<.05. These would change the analysis, not repair the evidence.

### Priority 3 — Fit and verify the final submission

1. Compress exhaustive robustness tables before cutting the expert protocol or fine result.
2. Put detailed per-expert scores, directional-only κ, exhaustive sensitivity values, and permutation size distributions in anonymous supporting material where permitted.
3. Build the paper and verify the inclusive page count.
4. Check each occurrence of “valid,” “robust,” “noise,” “driver,” “preserved,” and “significant” for the exact interpretation it implies.
5. Ensure title, abstract, discussion, conclusion, and practitioner notes tell the same bounded story.

The official guidelines request the initial abstract by 21 September 2026, 11:59 pm AoE. Use the current official submission page when confirming submission logistics rather than relying on older handoff dates. [LAK27 submission guidelines](https://www.solaresearch.org/events/lak/lak27/submission-guidelines/)

## 12. Final framing decisions

**Lead with:** an explicit relevance assumption, an auditable computational operation, and an evaluation that identifies where human alignment is supported and where it remains unresolved.

**Make prominent:** the coarse/fine distinction, the original and supplementary permutation interpretations, and the difference between aggregate stability and close-comparison sensitivity.

**Keep conditional:** conclusions about density assignment, taxonomy, expert consensus, and the curated sample.

**Avoid:** recovery of true teaching quality; proof of noise removal; validated fine ordering; “the null was verified”; “the coarse result is only a manipulation check”; “all results are exponent-independent”; claims that the negative finding itself demonstrates practical usefulness.

The intended reviewer takeaway is: **this is a substantive, inspectable method contribution whose evaluation is precise enough to constrain its interpretation.** That is the strongest foundation these results currently provide for a credible LAK submission.
