# LAK27 Full-Paper Framing and Source Map

## Working title

**Validity-Weighted Attenuation of Affective Noise in Open-Ended Teaching Feedback: An Interpretable ABSA Framework**

This deliberately avoids claiming that the method estimates *true teaching
quality*. It says what the study demonstrates: a transparent way to change the
modelled contribution of construct-irrelevant affect in rating-plus-text
feedback.

## Central claim

Open-ended teaching feedback contains both pedagogically actionable evidence
and broader affective student experience. Existing computational studies mostly
describe or predict from this text. We introduce **validity-weighted
attenuation**, an interpretable, clause-level method that proportionally
attenuates the modelled contribution of affect in content classified as outside
of a stated pedagogical taxonomy, while retaining the original review and a
review-level audit trail.

## Research questions

**RQ1.** How are topic-specific emotional signals associated with numerical
ratings in open-ended teaching feedback?

**RQ2.** How does validity-weighted attenuation change the modelled influence
of emotion in content classified as pedagogically miscellaneous?

**RQ3.** Does the mechanism exhibit behaviour consistent with its validity
rationale on held-out instructors, expert-labelled comparisons, and robustness
controls?

RQ3 deliberately asks about *consistency with a rationale*, not recovery of
true teaching effectiveness.

## Full-paper outline (target: 12--14 JLA pages inclusive)

### 1. Introduction (about 1.25 pages)

#### 1.1 Open-ended teaching feedback as a learning-analytics trace

Situate feedback as evidence used to understand and improve teaching. State the
practical tension: ratings are concise and consequential, while accompanying
text may mix instruction-relevant experience with other affective expression.

#### 1.2 The unresolved methodological gap

Prior NLP/ABSA work extracts sentiment, identifies topics, or predicts ratings;
it does not operationalize a transparent validity-oriented rule for interpreting
the relationship between text and a rating.

#### 1.3 Contribution and boundaries

List three contributions: (1) the attenuation mechanism, (2) its
psychometric/validity rationale and audit trail, and (3) empirical proof of
concept on a large, held-out-instructor sample with expert and robustness
evidence. State upfront that it is not a measure of true teaching quality and
is not proposed for automated high-stakes decisions.

### 2. Background and conceptual framing (about 1.5 pages)

#### 2.1 Validity, construct-irrelevant variance, and teaching feedback

Use Messick, Marsh and Roche, Wongsurawat, and relevant SET literature to
define the problem. Explain that validity concerns the interpretation and use
of scores, not a property bestowed on a dataset or algorithm.

#### 2.2 From descriptive NLP to validity-oriented interpretation

Condense the computational SET/ABSA review to establish the gap. Keep only
studies necessary to distinguish extraction/prediction from intervention on the
modelled influence of content.

#### 2.3 Design principle: attenuation rather than deletion

Explain why the method preserves raw feedback and emotional expression, uses a
bounded monotonic rule, and exposes each adjustment. State clearly that
"Miscellaneous" means outside this study's taxonomy, **not** unimportant to
the student experience.

### 3. Method (about 3 pages)

#### 3.1 Study context and data

Describe the RMP corpus, filtering, final analytic corpus, and why RMP is used
as a deliberately noisy stress-test rather than a proxy for institutional SET.

#### 3.2 Clause-level representation

##### 3.2.1 Clause extraction and pedagogical topic categorization

Describe the three pedagogical topics plus Miscellaneous, embedding method,
thresholding, and density calculation. Include the category table.

##### 3.2.2 Emotion extraction

Describe RoBERTa-GoEmotions outputs and topic-level aggregation.

#### 3.3 Rating model and evaluation split

Explain the feature matrix, CatBoost model, professor-level split and grouped
cross-validation. Emphasize that no review from held-out professors was used in
fitting.

#### 3.4 Validity-weighted attenuation

Give the fixed linear rule \(\zeta=1-D_{misc}\), the two model passes, and the
rating-delta calculation. Do not mention exponent tuning or optimization.

##### 3.4.1 Audit trail and worked examples

Use one compact worked example or a small table tracing clauses to categories,
density, attenuation, and delta. This is where interpretability becomes
concrete.

#### 3.5 Evaluation strategy

##### 3.5.1 Model behaviour

Held-out predictive performance; feature/correlation changes and delta patterns.

##### 3.5.2 Initial validity evidence

Expert paired comparisons, consensus rule, uncertainty intervals, and
inter-rater agreement. Include only final, rerun figures.

##### 3.5.3 Robustness controls

Fixed-positive-density permutation control and the fixed-rule sensitivity/
robustness evidence selected after the final rerun.

### 4. Results (about 2.25 pages)

#### 4.1 Corpus and model behaviour

Report corpus composition, held-out performance, and which topic-emotion
features drive ratings.

#### 4.2 What attenuation changes

Report the proportion affected, delta distribution, correlation/feature shifts,
and one or two contrasting examples. Use careful language: these are changes to
modelled contributions and ratings, not direct evidence of true quality.

#### 4.3 Initial validity and robustness evidence

Report multi-expert consensus accuracy with Wilson intervals, Fleiss' kappa,
and final permutation/sensitivity results. Explain the 77 evaluable pairs and
the three unmatched pairs once, transparently.

### 5. Discussion (about 1.5 pages)

#### 5.1 A new validity-oriented analytic primitive

Argue the contribution is an operational mechanism joining topic relevance to
the use of affective signals, rather than another sentiment classifier.

#### 5.2 Implications for responsible interpretation of teaching feedback

State the appropriate use: an auditable companion view for educators or
teaching-support staff. Preserve raw ratings/text and surface pedagogical and
other experience signals separately.

#### 5.3 Boundaries, risks, and non-use

It must not be used as an automated faculty-quality measure or personnel score.
Classification error, incomplete taxonomy, RMP self-selection, and broader
affective experience all constrain interpretation.

### 6. Limitations and future work (about 0.75 pages)

#### 6.1 Evidence limits

Single noisy platform, no external criterion of teaching quality, incomplete
topic taxonomy, and initial expert-validation sample.

#### 6.2 Method limits

Hard topic assignments, density as a relevance proxy, and the all-Miscellaneous
collapse point.

### 7. Conclusion (about 0.35 pages)

Restate the bounded contribution: a transparent proof of concept for
validity-weighted interpretation of rating-plus-text teaching feedback.

### Notes for Practitioners (required JLA element; about 0.25 pages)

**Users:** instructors and teaching/learning support staff interpreting open
feedback.

**Use:** inspect a review's original text, topics, and adjustment trail; use it
to distinguish potentially actionable pedagogical feedback from other student
experience signals.

**Do not use:** automated ranking, promotion, tenure, discipline, or any
high-stakes judgment about an instructor.

**Interpretation:** an attenuated value is a model-based alternative view under
a stated relevance taxonomy; it is not a validated estimate of teaching quality.

## What can transfer from the existing manuscript

| Existing material | Transfer decision | LAK treatment |
| --- | --- | --- |
| Introductory account of SET contamination and the three original RQs | **Revise** | Retain the problem and citations, but replace claims about improving "actual teaching effectiveness" with the bounded central claim above. |
| Contribution bullets in the introduction | **Revise** | Preserve the three contribution categories but foreground learning-analytics interpretation, auditability, and boundaries. |
| `Literature Review > SET Contamination` | **Mostly copy, then cut** | Directly reusable evidence and citations; reduce to the two or three paragraphs needed for the validity problem. |
| `Literature Review > Computational SET Analysis` | **Revise heavily** | Keep only the progression needed to establish that prior work is descriptive/predictive; remove broad model-by-model history. |
| `Literature Review > Computational Validity Analysis` | **Mostly copy, then cut** | Retain direct comparison to work that finds bias or adjusts scores, making the mechanism gap explicit. |
| `Literature Review > Psychometric Validity & Explainable Intervention` | **Copy-ready core** | The Messick/Cronbach/Huber rationale is the theoretical spine. Copy the strongest passages, then add the caveat that relevance classification is a design choice. |
| Dataset, cleaning, corpus description, and descriptive figures | **Copy-ready factual core** | Update only for JLA formatting and concise presentation. Keep the corrected 17,127-review count consistent everywhere. |
| ATC, emotion, regression, and attenuation methods | **Copy-ready factual core** | Transfer equations, implementation details, category definitions, and professor-level-split justification. Delete all obsolete exponent-selection language. |
| Pseudocode and worked examples | **Copy selectively** | Use the pseudocode if it fits; retain only one compact, high-value worked example in the main paper. Move extra examples to supplement/repository if allowed. |
| Regression, SHAP, correlation, and delta results | **Revise / verify** | Reuse final figures/tables only after confirming they match the fixed linear rule and final regenerated outputs. Avoid a figure gallery. |
| Expert-validation results | **Do not copy yet** | Replace entirely with final multi-expert consensus, Wilson intervals, Fleiss' kappa, and the clear 77/80 accounting. |
| Robustness material | **Do not copy yet** | Use only final post-correction results from the fixed-positive-density permutation design. |
| Discussion | **Rewrite** | Keep useful interpretations, but make responsible teaching-feedback interpretation—not a claim of recovered truth—the focus. |
| Limitations and future work | **Mostly copy, then prioritize** | The honest limitations are valuable. Cut proposals that consume space; elevate external-criterion and taxonomy limitations. |
| Ethical considerations and data/code availability | **Copy-ready with de-identification check** | Preserve REB/exemption and access statements, ensuring double-blind wording and repository visibility follow submission rules. |

## Material that must not enter the LAK draft unchanged

- Any claim that adjusted ratings reflect, recover, or better measure **actual
  teaching quality**.
- Any statement that Miscellaneous content is inherently irrelevant,
  unimportant, or invalid student voice.
- Exponent tuning, grid-search, or old `s=0.83` descriptions/results. The
  operative method is fixed and linear (`S_VALUE = 1.0`).
- Superseded robustness results in `newresults.md`.
- Single-expert results presented as the final validation evidence once the
  consensus analysis is available.
- Identifying institutional/author information, acknowledgements, or a public
  repository link in the double-blind version.

## Drafting rule

For every claim, distinguish among:

1. **Observed:** a result in this corpus;
2. **Modelled:** a change produced by the specified method; and
3. **Aspirational:** a potential future validation or application.

This distinction will protect the paper's credibility while allowing the
methodological novelty to remain the centre of the submission.

## Citation strategy: add a lean LAK anchor, not a new literature review

The current bibliography is already strong on SET validity, psychometrics, and
NLP/ABSA. The LAK draft needs a small number of learning-analytics citations so
the work is visibly situated in the field. Add the following sources only where
they advance an argument; do not pad the bibliography.

| Source | Where to cite it | Function in the paper |
| --- | --- | --- |
| Gašević, Dawson, & Siemens (2015), *Let's Not Forget: Learning Analytics Are about Learning* | Introduction, Section 1.1 | Establishes that LA must connect analytical work to learning and teaching, not only computational performance. |
| Lockyer, Heathcote, & Dawson (2013), *Informing Pedagogical Action: Aligning Learning Analytics with Learning Design* | Introduction or Discussion 5.2 | Grounds the claim that the intended contribution is more cautious pedagogical interpretation/action. |
| Ferguson & Clow (2017), *Where Is the Evidence? A Call to Action for Learning Analytics* | Discussion 5.1 and Limitations 6.1 | Supports the bounded proof-of-concept framing; this paper provides initial method evidence, not an evaluated intervention. |
| Drachsler & Greller (2016), *Privacy and Analytics: It's a DELICATE Issue* | Discussion 5.3 / Notes for Practitioners | Supports transparency, stated purpose, stakeholder access, and governance. |
| Prinsloo & Slade, *Ethics and Learning Analytics: Charting the (Un)Charted* | Discussion 5.3 | Supports non-use, possible harms, and contestability in institutional interpretation of data. |
| Tsai & Martinez-Maldonado (2022), *Human-centered Approaches to Data-informed Feedback* | Discussion 5.2 (optional) | Supports the human-in-the-loop framing: the method assists sensemaking, not judgment automation. |

Suggested LAK-anchoring paragraph for the introduction:

> Learning analytics concerns the interpretation of educational data to
> understand and improve learning and teaching contexts. Its contribution
> therefore depends not only on analytical performance, but also on its
> connection to pedagogical action, stakeholder interpretation, and responsible
> use. In this study, we treat open-ended teaching feedback as a trace requiring
> cautious, auditable interpretation rather than as a direct measure of
> instructor quality.

Use the first, second, and fourth sources in that paragraph or its surrounding
sentences. Cite Ferguson and Clow in the limitations rather than pretending the
paper demonstrates intervention impact.

If space is needed, remove broad, model-by-model computational SET citations
before cutting the core SET-validity, psychometric, or LAK-anchor citations.

### Essential adjacent-method citations

Use these two papers in Section 2.2 (*From descriptive NLP to validity-oriented
interpretation*). **Ren et al. (2022) is already in the manuscript bibliography:**
retain it and make its contrast more explicit. Add Butt et al. (2025). Neither is
a threat to the paper's contribution; together they make the gap concrete and
credible.

| Source | What it establishes | Precise contrast to state |
| --- | --- | --- |
| Ren, Yang, & Luo (2022), *Automatic Scoring of Student Feedback for Teaching Evaluation Based on Aspect-Level Sentiment Analysis*, *Education and Information Technologies*, 28, 797--814. https://doi.org/10.1007/s10639-022-11151-z | Aspect-level sentiment analysis can turn free-text SET comments into aspect scores and richer feedback. | The method extracts and aggregates aspect sentiment; it does not use the relevance of text to proportionally attenuate the modelled contribution of affect to an accompanying numerical rating. |
| Butt, Núñez-Daruich, Alvarado-Uribe, & Ceballos (2025), *Cutting-Edge Technologies for Analyzing Student Feedback to Inform Institutional Decision-Making in Higher Education*, *Foresight and STI Governance*, 19(4), 68--80. https://doi.org/10.17323/fstig.2025.28047 | Modern ABSA/LLM systems can segment and classify SET opinions into pedagogical aspects for actionable insight. | The framework produces structured insights; it does not propose or evaluate a validity-weighted, review-specific rule for recalibrating the modelled role of affect in ratings. |

Suggested transition sentence:

> Recent aspect-based approaches demonstrate that open-ended teaching feedback
> can be segmented and organized into pedagogical aspects. However, extracting
> structured sentiment is not itself a validity intervention: these approaches do
> not specify how the pedagogical relevance of a clause should change the
> contribution of its affective content when interpreting the numerical rating
> that accompanies it.

Follow this sentence with Ren et al. (2022) and Butt et al. (2025), then present
validity-weighted attenuation as the response to this unaddressed question.
