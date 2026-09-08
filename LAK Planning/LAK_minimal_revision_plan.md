# LAK manuscript: minimal substantive revision plan

Prepared 8 September 2026 against `LAK_draft/main.tex`, the supplied expert/robustness results, and the author's density-only baseline output. Updated after the author's manual revisions on 8 September 2026. Progress below reflects the saved manuscript at this checkpoint; earlier proposed wording is guidance, not evidence that a change was applied. Baseline results below were supplied by the author, not independently rerun for this plan.

## Scope: all original review findings, plus the density-only results

This plan covers the full initial review, not only the new baseline comparison. “Minimal” refers to the size of the remedy for each issue, not to omitting issues. Every item in the checklist below requires a manuscript response. New data collection is needed only if retaining a claim that the existing evidence cannot support; narrowing that claim is the default remedy for this revision.

## Objective and editorial decision

Produce one coherent proof-of-concept paper with the smallest set of substantive changes that addresses the strongest foreseeable reviewer objections. These changes are intended to improve the acceptance case; they cannot guarantee acceptance.

Keep the attenuation mechanism, dataset, fitted model, grouped evaluation, expert study, and robustness analyses. Reframe their interpretation, add the completed density-only comparison, and make the educational purpose explicit. No new model training, expert recruitment, or deployment study is required for this revision unless the targeted checks below reveal a substantive error.

The central contribution is an auditable, taxonomy-conditioned method for examining rating sensitivity, accompanied by initial expert comparison and a reproducible baseline for subsequent research. The current evidence does not establish that the adjusted ratings are better measurements of teaching or that the full mechanism improves expert-ranking agreement over density alone.

Suggested central claim:

> We introduce an auditable method for examining how a rating model responds when affect outside an explicit pedagogical taxonomy is attenuated. An RMP proof of concept characterizes its behaviour and establishes an initial expert-comparison baseline: density alone matches the full mechanism's aggregate agreement on the selected pairs, while the incremental value of model-based adjustment remains unresolved.

Future research is a legitimate beneficiary of the baseline, but the paper must also explain its present contribution: the explicit transformation, traceable outputs, evaluation protocol, and empirical boundary identified by the comparison. A future-work promise cannot substitute for that explanation.

## Current progress and next-session handoff

This checkpoint supersedes the original ordering below. Sections 1–9 retain the complete scope and detailed guidance; use the status checklist to avoid repeating finished edits. Line numbers refer to the saved 800-line manuscript at this checkpoint and must be rechecked after edits.

### Working agreement

- The author edits the manuscript manually. Supply the current line number, replacement boundary, and exact LaTeX text, one change at a time unless a batch is requested.
- Do not edit the manuscript or render the PDF. This update changes only the revision plan.
- Prefer positive, substantive statements to repeated explicit negations. Preserve relevant LAK citations and the proposed auditable review-queue application.
- Read the current file before proposing a replacement. The author has adapted several suggestions; those saved choices take precedence over earlier proposed versions.
- “Minimal revision” means targeted remedies for all identified issues, not omission of inconvenient findings. No new model fitting or exponent tuning is planned.

### Completed local edits — preserve these

- Expert table now compares attenuation and density alone on the same pairs: 64/77 overall, 43/43 coarse, 21/34 fine for each. The caption defines both rankings and labels expert kappa clearly.
- Results report 61 shared successes and three exclusive successes per method. The two density ties and unchanged tie-sensitivity result are documented.
- The abstract reports the density-only match and accurately describes expert judgment versus adjustment ordering. Other abstract claims remain to be revised.
- The introduction now defines **taxonomy-excluded affect** and describes the model-based adjustment, audit trail, and proposed human-review workflow.
- RQ2 now includes held-out model behaviour and perturbation stability. RQ3 concerns expert alignment. Contribution bullets now include an expert protocol and density reference, although specific wording still requires checks below.
- The validity definition now concerns evidence for interpretations and uses. The Huber discussion motivates down-weighting; the old direct Cronbach justification has been removed from the core method.
- The taxonomy explanation recognizes omitted pedagogical concerns, ambiguity, and classifier error. The density definition describes an operational share of text.
- The attenuation description now identifies a fitted-model response, fixed remaining inputs, nonlinear interactions, and retention of the original prediction residual.
- The exponent paragraph correctly describes a family of weighting curves with linear attenuation at s = 1.
- The expert comparison's linking hypothesis is explicit. Existing method/limitations text discloses that expert pairs span training and held-out instructors.
- Discussion includes the density reference for future research and identifies signed-adjustment usefulness as a separate evaluation question.

These are completed passages, not confirmation that every related claim elsewhere is aligned. In particular, the taxonomy/mechanism category is substantially repaired locally but still needs the worked-example review, citation verification, and terminology consistency. Earlier conversation statements calling that whole category complete were too broad.

### Remaining work, ordered by payoff

| Order | Current location | Action |
|---|---|---|
| 1 | Discussion, lines 695–705 | Reorganize around revised RQs. Put coherence, permutation dependence, exponent sensitivity, and conditional bootstrap stability under RQ2. Give expert agreement and the density comparison a focused RQ3 interpretation. |
| 2 | Lines 699, 683–687, 614 | Remove Wilson-interval inclusion as evidence of exponent equivalence; separate bootstrap sampling stability from exponent sensitivity; retain individual sensitivity alongside small average differences; qualify unsupported explanation of rank behaviour. |
| 3 | Conclusion, lines 766–770 | Mirror current contributions, include the baseline finding, and remove the superseded Cronbach bridge and noise-correction narrative. |
| 4 | Title/abstract, lines 56 and 102; terminology throughout | Align with the saved definition of taxonomy-excluded affect. “Taxonomy-defined noise” remains in the abstract, example, results, discussion, limitations, and conclusion. Recast claims about average conservatism and measurement improvement. |
| 5 | Implications, lines 709–719 | Preserve the review queue and LAK citations, identify the proposed inspection benefit, and describe configurable taxonomy as a design feature rather than a second established theoretical contribution. |
| 6 | Example/evaluation, lines 352, 416, 556–560 | Discuss contestable example assignments; describe LLM agreement as consistency evidence; retrieve actual expert instructions and clarify selection/verification. |
| 7 | Availability and end matter, lines 782–792 | Resolve funding, anonymous access, actual reusable evaluation materials, and documented ethics statements; perform source/layout checks within the author's rendering preferences. |

**Recommended next change:** the discussion block at lines 695–705. Propose it in manageable parts under the author's approval/manual-edit workflow. The author requested analysis and this plan update; replacement discussion text has not yet been proposed or approved.

### Small remaining introduction decisions

- Lines 128 and 164 retain “offers no mechanisms” and “the first.” Verify their exact literature scope or qualify them; the introduction's main argument is otherwise revised.
- Line 165 says **pre-specified sensitivity checks**. This is a claim about the study timeline. Confirm it from existing records or use “sensitivity checks.” Do not infer prespecification from selecting s = 1 a priori.
- Line 154's RQ3 currently omits the explicit density comparator. Recommend adding “compared with density alone,” preserving the author's preferred wording around it.
- Lines 169–175 now contain a roadmap, rather than the earlier proposed review-queue paragraph. Narrow “ordering properties that do not exceed a density-only reference” to matched aggregate agreement on the selected pairs. Describe a reusable protocol/reference rather than implying a validated evaluation instrument.
- Lines 207–218 now supply a taxonomy rationale citing Marsh1982. Verify that the source supports the particular dimensional mapping and describe the actual design history accurately. The rationale exists; it should not be requested again as if absent.
- The author has retained the method name **validity-weighted attenuation**. Renaming remains a recommendation, not an approved decision.

### Evidence/reporting checks still open

No new outcomes from these checks have been provided in this session:

- Review the six exclusive-success pairs and the unanimous expert/model disagreements, including the worked example's category boundaries.
- Retrieve the expert task wording, what experts saw, how “validity” was explained, and the ATC-verification/selection details.
- Establish whether threshold-development clauses overlap the reported classification evaluation.
- Verify the denominator for mean absolute adjustment, how values outside 1–5 are treated, and the SHAP target/reference and importance normalization.
- Verify source support for the Marsh/Roche correction paraphrases and the taxonomy citation.
- Confirm access to labels, pair membership, density, deltas, instructions, script, and appropriate text access before claiming reproducible reuse.
- The previous saved log recorded 16 pages, above the supplied full-paper call's 14-page maximum. That log predates later edits and is not a current page count. Plan to shorten repetitive discussion/caveats and have the author check layout when ready; do not compile automatically.

The density-only output has 154 distinct reviews with no repeated review across pairs. This does not establish absence of instructor clustering. The reported exact McNemar p = 1 is available but need not be added to the manuscript if paired counts and the limited inference are clearly reported. No density-only permutation test has been reported.

## Complete issue-to-change checklist

Status: **[x]** = addressed in the saved manuscript; **[~]** = partially addressed, with related passages/checks still open; **[ ]** = open. The checkpoint above records the remaining work for partial items. The numbered sections retain the original implementation guidance, including proposals that the author has adapted.

| Done | Finding from the initial review or subsequent baseline analysis | Required manuscript response | Minimum remedy |
|---|---|---|---|
| [~] | Three competing stories: rating correction, model sensitivity, and educator support | Establish model sensitivity as the empirical object and educator interpretation as the proposed purpose; remove unsupported measurement-improvement promises | Align opening and closing claims across sections |
| [~] | Strong introduction followed by repeated retreat in limitations | State the intended interpretation and evidential scope at the outset | Rewrite the gap and abstract; consolidate later caveats |
| [ ] | Title implies measured validity weights and identified affective noise | Use a title and method description consistent with taxonomy-conditioned, validity-informed attenuation | Retitle or explicitly qualify the retained method name |
| [~] | Broad novelty claim rests on correcting ratings | Define the specific computational and evaluative contribution without relying on an unsupported first-ever claim | Replace contribution bullets; qualify literature gap |
| [~] | Experts judged review validity, not rating adjustments | Describe the actual expert task and distinguish it from the model-derived comparison | Correct abstract, Method, Results, and conclusion wording |
| [~] | Smaller absolute adjustment is treated as inherently greater validity | State this as the tested linking hypothesis and explain why it can fail | Add a short rationale and boundary statement |
| [~] | Expert results do not validate adjustment direction, amount, or improved teaching measurement | Remove those implications wherever they occur | Explicitly delimit what the expert study supports |
| [x] | Overall 83.1% depends on curated coarse/fine composition | Report selection and subgroup counts beside overall agreement | Limit inference to the evaluated sample |
| [~] | Expert pair selection uses model outputs and verified ATC assignments | Explain selection, verification, and conditioning on screened classifications | Add protocol details and limitations |
| [x] | Expert sample spans training and held-out instructors | Separate sample descriptions for prediction/coherence and expert analyses | Correct any blanket held-out validation claim |
| [~] | High-contrast alignment and unresolved fine comparisons are not central enough | Make the contrast a finding, without presenting 0.5 as a validated threshold | Rewrite RQ3 and its discussion |
| [~] | Taxonomy exclusion is conflated with pedagogical irrelevance and CIV | Separate operational category membership from construct relevance | Correct definitions and interpretation throughout |
| [~] | Intended educational interpretation and taxonomy rationale are underspecified | State the limited interpretation served and the actual basis for selecting the categories | Add one focused rationale paragraph |
| [x] | Residual category mixes irrelevant content, missing dimensions, and classifier error | Identify these distinct sources and the risk of construct underrepresentation | Add to taxonomy explanation and limitations |
| [ ] | Worked example's category boundaries are contestable | Discuss the rude-person remark and subject-knowledge clause as model decisions requiring inspection | Revise example commentary without changing underlying outputs |
| [x] | Validity is described as a property of elicited content alone | Restore validity as evidence supporting interpretations and uses | Replace the incorrect theoretical sentence |
| [~] | Prediction perturbation is treated as removal of actual rating contamination | Describe Delta as a fitted-model response to specified input scaling | Replace correction/causal language in Method and claims |
| [x] | Residual retention is implicit | Explain that raw-minus-predicted residual is carried into the adjusted value and is not established to be contamination-free | Add one sentence after the adjustment equation |
| [~] | Fixed pedagogical inputs are treated as unchanged pedagogical contributions | Acknowledge nonlinear interactions and distinguish input invariance from contribution preservation | Correct the “changes only” sentence and related RQ2 claims |
| [~] | SHAP/correlation changes substitute for improved measurement | Classify these as mechanistic coherence checks | Revise result interpretation and discussion hierarchy |
| [~] | Permutation changes density both as predictor and weight | State the tested perturbation and avoid claiming isolation of the weighting mechanism | Clarify Method and interpretation |
| [x] | Huber is presented as prescribing linear density weighting | Describe a motivated design choice rather than a derivation or guarantee | Rewrite theoretical bridge and exponent introduction |
| [~] | Cronbach is used as direct justification for the transformation | Remove the unsupported direct justification | Retain only source-supported reliability context, if needed |
| [ ] | Wilson interval inclusion is used to imply equivalence across exponents | Remove that inference | Report observed ranges descriptively |
| [ ] | Fixed-pipeline professor bootstrap is overgeneralized | Restrict its meaning to conditional sampling stability | Correct bootstrap and discussion wording |
| [ ] | Small mean and preserved distribution imply uniformly conservative adjustment | Restrict the claim to average behaviour and retain individual sensitivity | Correct abstract/results/discussion wording |
| [~] | LAK purpose arrives mainly in implications | Introduce a concrete educator inspection task early | Add the use case to the problem statement and align practice notes |
| [ ] | Proposed review queue could be mistaken for validated usefulness | Distinguish potential workflow from evaluated impact | Qualify the implications paragraph |
| [x] | Full mechanism lacks a simple comparator | Integrate the completed density-only comparison | Extend existing expert table and add a short baseline paragraph |
| [~] | Density matches overall and subgroup accuracy | State no observed ranking-agreement advantage, while distinguishing untested additional outputs | Update abstract, discussion, and conclusion |
| [x] | Equal accuracy/p = 1 could be mistaken for equivalence | Report paired wins/losses and avoid an equivalence claim | Add one sentence and retain exact test as descriptive support |
| [ ] | Original permutation advantage could be mistaken for superiority over density alone | Explain that dependence on original density is a different comparison | Add the baseline-aware interpretation |
| [~] | Future baseline contribution could be overstated | Call it an initial curated-sample reference and document model-based selection | Qualify benchmark language and describe reuse limits |
| [ ] | Reusable evaluation contribution depends on actual materials | Verify anonymous release of instructions, pairs, labels, scores, and code with accurate access restrictions | Repair availability statement and supplement |
| [~] | Mechanism's additional value remains unresolved | Explain what signed adjustments and audit trails add as outputs, without claiming demonstrated educational benefit | State present contribution and targeted future evaluation |
| [ ] | Error cases may reveal substantive taxonomy or mechanism problems | Inspect exclusive successes and unanimous disagreements; report limitations honestly | Targeted review of existing cases, not a broad new study |

## 1. Original revision scope — consult the checkpoint for current priority

| Priority | Location | Minimum required change | Reviewer objection addressed |
|---|---|---|---|
| 1 | Abstract, expert results, discussion, conclusion | Integrate density-only comparison and its implications | The full pipeline is presented as validated without testing a simple alternative |
| 2 | Title, introduction, contributions, terminology throughout | Align claims with model sensitivity and initial comparative evidence | The paper promises measurement correction but evaluates model behaviour and review judgments |
| 3 | Background, taxonomy method, worked example | Specify intended interpretation and distinguish taxonomy coverage from construct relevance | Miscellaneous content is assumed to be invalid or irrelevant |
| 4 | Attenuation method and RQ2 interpretation | Describe the actual mathematical operation and its limits | Feature perturbation is treated as identified removal of rating contamination |
| 5 | Expert method and research questions | Explain the judgment-to-ranking hypothesis and selection protocol | Experts are portrayed as validating adjustment direction or magnitude |
| 6 | Robustness and discussion | Correct overinterpretations; shorten repetitive statistical defence | Dependence and stability are treated as independent validity evidence |
| 7 | Introduction, practice notes, implications | State a concrete educator interpretation task and distinguish proposed use from evaluated use | LAK relevance appears only as a late application claim |
| 8 | Availability statements and final checks | Make the claimed evaluation resource reproducible and remove submission blockers | The baseline cannot be reused or key methodological details are missing |

## 2. Report the completed density-only comparison

**Status:** implemented in the expert table, caption, tie description, result paragraph, and abstract. Preserve those additions. Discussion/conclusion alignment and verification of reuse materials remain open. The numerical reference and wording guidance below are retained for checking.

Baseline: the review with lower `D_misc` is predicted to be the more valid review. Comparator: the review with smaller absolute model adjustment is predicted to be more valid. Use identical expert consensus, evaluable pairs, and original model-defined coarse/fine groups.

| Condition | Pairs | Attenuation correct | Density-only correct | Agreement for each |
|---|---:|---:|---:|---:|
| Overall | 77 | 64 | 64 | 83.1% |
| Coarse | 43 | 43 | 43 | 100% |
| Fine | 34 | 21 | 21 | 61.8% |

Paired correctness: 61 pairs correct for both methods, 3 correct only for attenuation, 3 correct only for density, and 10 incorrect for both. All six exclusive successes occur in the fine group. Exact two-sided McNemar p = 1.000; this is not an equivalence test. The observed accuracy difference is zero.

Density has two exact ties; attenuation has none. Counting exact ties as incorrect rather than selecting displayed review 1 leaves these results unchanged. There are 154 distinct reviews in 77 pairs, with no review reused. Instructor overlap has not been established by this output; do not claim full pair independence from review uniqueness alone.

Suggested results language:

> Density alone matched attenuation's aggregate agreement overall (64/77) and in both contrast groups. Each method correctly ranked three pairs that the other did not. Thus, this evaluation provides no observed agreement advantage for the full mechanism over the density-only baseline. The comparison establishes an initial reference for subsequent methods on this curated sample; it does not establish statistical equivalence.

Suggested abstract sentence:

> Adjustment-magnitude ordering agreed with expert relative-validity judgments on 83.1% of 77 selected pairs, matching a density-only baseline; fine-pair agreement for attenuation did not exceed its permutation benchmark.

Important limits:

- Do not call 83.1% a general population accuracy or a field-wide benchmark.
- Do not infer that the two methods make identical predictions from identical accuracy or paired correctness alone.
- Do not claim that the density-only fine result was permutation-tested; the existing permutation results concern attenuation.
- Report this as an additional analysis, not as a preregistered or originally planned baseline.
- Do not tune the exponent or taxonomy against these same labels and present the result as independent validation.

## 3. Align title, gap, questions, and contributions

### Title and terminology

Recommended title:

> Validity-Informed Attenuation in Teaching-Feedback Analytics: An Auditable Framework and Initial Expert Comparison

Prefer “validity-informed attenuation” in the text: it describes the motivation without implying that validity itself was measured as a weight. Existing code names do not need changing. If retaining “Validity-Weighted Attenuation” as the method's established name, explicitly identify the weight as a taxonomy-derived density proxy and avoid claiming measured validity.

Use “content outside the stated taxonomy,” “miscellaneous-category affect,” and “model-based adjustment” where they describe the operation. Reduce reliance on “noise,” “contamination,” and “correction” as labels for what the system has identified. Reserve construct-irrelevant variance for the motivating validity concern, conditional on a specified interpretation.

### Introduction and research gap

Replace the broad progression “descriptive methods leave contamination uncorrected; we intervene to correct it” with a narrower gap: existing topic/sentiment summaries do not necessarily expose how an explicit relevance assumption changes a modelled rating summary.

Introduce the intended educator task here: inspecting reviews whose modelled rating is sensitive to attenuation, using the original text and audit trail to assess the interpretation. Identify this as a proposed use. The expert task has not demonstrated improved review prioritization, educator decisions, or learning outcomes.

Avoid an unsupported field-wide “first” claim. State the concrete combination the paper contributes; retain a priority claim only if the literature supports its exact scope.

### Research questions

Keep three questions and the existing section structure where possible:

1. **RQ1:** What topic-specific affective patterns characterize the feedback, and how are they associated with ratings in the fitted model?
2. **RQ2:** How does taxonomy-conditioned attenuation change model outputs and feature associations on held-out instructors, and how stable are these patterns under the tested perturbations?
3. **RQ3:** How does adjustment-magnitude ordering align with expert relative-validity judgments, compared with density alone, across the selected contrast groups?

This moves robustness under RQ2 and gives the expert/baseline comparison a clear target under RQ3. Descriptive results become context; the transformation and comparative evaluation carry the contribution.

### Contributions

Replace the current three claims with:

- An explicit attenuation mechanism linking a stated relevance taxonomy to traceable model-based rating changes.
- A proof-of-concept characterization of its behaviour on an RMP corpus, including held-out-instructor analyses and specified robustness checks.
- An initial expert-comparison protocol and density-only reference result that identify what is supported and what remains unresolved.

Claim a reusable annotated resource only after verifying the release described in Section 8 below. Do not call configurability alone a second theoretical contribution or imply the expert sample is wholly held out.

## 4. Repair the validity and taxonomy argument

Make a short, explicit distinction between:

1. The intended interpretation: feedback concerning the instructional dimensions represented by this study's taxonomy.
2. The operational proxy: word share assigned outside those categories by a thresholded classifier.
3. The motivating concern: information irrelevant to a specified interpretation can compromise score meaning.

The proxy does not establish the concern in each review. The residual category may include omitted pedagogical dimensions, ambiguous wording, or classification errors. These possibilities create a risk of construct underrepresentation as well as imperfect detection of irrelevant content.

Required edits:

- Replace “Validity is thus a property of the content an instrument elicits” with a statement about evidence supporting score interpretations and uses; content coverage is one component.
- State why the three included dimensions were chosen, based on the actual design history. Do not invent stakeholder co-design or theoretical derivation.
- Describe the taxonomy as a limited operational lens, not a comprehensive definition of teaching quality or pedagogical relevance.
- Explain that agreement between two LLMs is inter-model consistency, not independent proof of category validity.
- Keep the human classification results visible. Verified ATC assignments in the expert-pair sample condition that evaluation on a screened subset; they do not validate ordinary pipeline error rates.

Worked example: “is a rude guy” is assigned to Miscellaneous, while “he knows alot about politics” is assigned to Instructional Effectiveness. Preserve the actual outputs and acknowledge their contestability. Explain that interpersonal conduct can be pedagogically relevant and subject knowledge is not synonymous with effective instruction. This can illustrate the purpose of inspection rather than being presented as an unquestionably correct adjustment. Do not manually alter labels while retaining the old numerical trace.

## 5. Correct the mechanism's interpretation and theoretical support

Keep the equations unchanged unless an implementation discrepancy is discovered.

Replace the claim that the procedure changes “only the model-estimated influence” of miscellaneous sentiment with:

> The adjustment is the difference between the fitted model's predictions before and after scaling the miscellaneous emotion features. Other input features remain fixed, although their contributions may interact with the changed features in the nonlinear model.

Explain briefly that adding this difference to the raw rating retains the original prediction residual. It is a model-based alternative summary, not an identified decomposition of true teaching signal and contamination. Scaling features can also produce combinations whose predictive interpretation has not been externally validated.

Revise the theoretical bridge:

- Messick motivates scrutiny of the intended interpretation, coverage, and evidence.
- Robust estimation supplies a broad motivation for considering downweighting; the manuscript does not derive this particular transformation from Huber's estimator.
- `1 - D_misc` is a transparent linear design choice, not a measured reliability coefficient or a theoretically mandated optimal weight.
- Remove claims that Cronbach (1951) directly justifies this adjustment or that downweighting universally yields less bias than exclusion.
- Call `1 - D_misc^s` a family of attenuation functions; only `s = 1` is linear in density.

Audit the exact Marsh/Roche paraphrases and page references before retaining claims that they specifically recommend this type of correction. The minimal fallback is to retain only claims directly supported by the source.

## 6. Clarify expert evaluation and robustness without expanding the study

### Expert protocol

Move or summarize the protocol in Method; retain outcomes in Results. Report the actual instruction/rubric, what experts saw, what “valid” meant in that instruction, selection and ATC-verification procedures, and whether the taxonomy was supplied to experts. Retrieve these from existing materials; do not retrospectively redefine the task.

Make the linking hypothesis explicit: reviews judged relatively more valid are hypothesized to receive smaller absolute adjustments. This is not guaranteed by the mechanism. Small adjustments can also arise from weak affect or the fitted model's local response.

State that the task evaluates ordering, not adjustment sign, exact amount, teaching quality, or stakeholder usefulness. Retain the mixed training/held-out sample disclosure and model-defined selection. The 0.5 cutoff defines this evaluation's groups; it is not an estimated discrimination or deployment threshold.

Keep expert kappa separate from method accuracy. Excluding non-directional votes changes the agreement question; it should not be used to explain away primary disagreements. Condense that sensitivity analysis or move detail to supplementary material if needed.

### Robustness interpretation

- Keep permutation findings as dependence on the original density assignment under the specified perturbation. State that density is shuffled as both a model predictor and an attenuation input, so this does not isolate the weighting step.
- Add that the permutation result does not establish superiority over the density-only baseline.
- Retain both subgroup specifications transparently. Fixed and recomputed membership answer different questions; do not silently replace the originally primary specification because the fixed result is more favourable.
- Remove the argument that other exponents lying within the operating point's Wilson interval establishes comparable performance. Report the observed range descriptively.
- Describe professor bootstrapping as sampling stability conditional on the fitted pipeline, not robustness to taxonomy error or proof of stability across exponents.
- Describe small mean adjustments as small on average. Do not infer universal conservatism from the mean or preserved distribution shape; retain the material individual sensitivity already reported.
- Keep SHAP/correlation shifts as coherence evidence. Fixed pedagogical inputs do not guarantee preservation of all pedagogically valid information.

## 7. Small checks with high editorial value

These are narrowly scoped checks of existing materials, not a new experimental programme.

- [ ] Inspect the six pairs with exclusive method successes. Record why density and attenuation differ, including affect, density, and taxonomy assignment. Report any interpretation as post hoc; do not infer a general advantage from three favourable cases.
- [ ] Check the unanimous expert/model disagreements and the worked example for consequential category-boundary issues. If systematic omission of relevant content is evident, narrow the intended interpretation or revise the taxonomy and rerun affected outputs. A disclaimer alone cannot justify a misleading interpretation.
- [ ] Clarify whether the development clauses used to choose the similarity threshold overlap the reported classification evaluation. Disclose any overlap.
- [ ] Verify whether the reported mean absolute adjustment is across all reviews or only the miscellaneous/adjusted subset; use the correct denominator everywhere.
- [ ] Clarify how adjusted values outside the original 1–5 scale are handled. Do not add clipping merely to make outputs look conservative; changing the operation requires updated results.
- [ ] Clarify the SHAP comparison's output target, background/reference, and absolute versus normalized importance. Do not describe a prediction explanation as an explanation of the residual-added adjusted score without justification.

If unavailable evidence blocks a claim, narrow or remove the claim. Do not fabricate protocol details or turn every reporting gap into a new study.

## 8. LAK relevance, reproducibility, and submission readiness

Retain one concrete workflow throughout the paper: an educator inspects the original text, topic assignments, affective profile, and model-based adjustment to judge whether the proposed interpretation is appropriate. A review queue is a possible interface for this task; its effectiveness remains future work. Avoid portraying miscellaneous content as feedback to ignore.

Consolidate repeated cautions into a clear interpretation statement near the method and a focused limitations paragraph. Keep the existing prohibition on automated consequential instructor judgments. Use the saved space for the baseline and taxonomy rationale.

Before describing the study as providing a reproducible reference, verify that the anonymous supplement/repository includes:

- [ ] Expert instructions and annotation response definitions.
- [ ] Pair membership, orientation, expert labels, and selection/verification description.
- [ ] Density scores and saved deltas needed to reproduce both rankings and original bins.
- [ ] Tie, majority, exclusion, and scoring rules plus the baseline script.
- [ ] A permitted, privacy-appropriate way to inspect the evaluated material. Numeric inputs suffice to reproduce scores, but substantive reuse for new text methods requires access to the relevant text or an authorized linkage route. Describe any restrictions accurately.
- [ ] The baseline output archived with the input/code version; no claim that the analysis was prespecified.

Final manuscript checks: fill the funding placeholder, provide an actual anonymous availability link, remove drafting colours/TODOs, verify references and quotes, compile, and check the applicable page limit. Confirm the factual basis of the existing ethics/exemption and data-availability statements; do not strengthen them beyond the documentation.

## 9. Optional work to defer

Do not make these prerequisites for the focused revision:

- New expert recruitment or a large independently sampled benchmark.
- New model architectures, retraining, or exponent optimization.
- A full taxonomy redesign or broad threshold sweep absent evidence requiring it.
- A deployment, educator usability study, or external teaching-quality validation.
- A new interface, multiple new figures, or a wholesale reorganization of the paper.

These are appropriate future directions. The present paper should identify the particular unresolved question each would address: independent generalization, classification sensitivity, value beyond density, or defensibility/usefulness of signed adjustments.

## 10. Revision sequence and completion criteria

1. Revise the discussion around current RQ2/RQ3 and integrate the density baseline's meaning.
2. Correct statistical interpretations in the discussion and corresponding robustness passages.
3. Align the conclusion, then title/abstract and remaining terminology with the revised body.
4. Resolve the small introduction decisions and preserve the educator review-queue use case with its LAK citations.
5. Complete targeted example, protocol, source, and reporting checks; consolidate repeated material for length.
6. Verify anonymous evaluation materials and submission details. PDF rendering remains the author's task unless newly authorized.

The revision is complete when a reviewer can accurately summarize it as follows:

> The paper proposes a traceable, taxonomy-conditioned attenuation operation for teaching-feedback analytics, characterizes its behaviour, and supplies an initial expert comparison with a simple baseline. Density alone matches aggregate expert-ranking agreement on the selected pairs, making the added value of rating adjustment an explicit open question. The work provides a concrete mechanism and evaluation reference without claiming validated teaching-quality correction.

Residual acceptance risk: some reviewers may still find the method's practical value or incremental contribution insufficient without a study targeting the additional outputs. Honest framing reduces the mismatch between claims and evidence; it cannot manufacture evidence of usefulness. The strongest minimal revision makes the existing contribution precise and reproducible, rather than promising that future research will establish it.
