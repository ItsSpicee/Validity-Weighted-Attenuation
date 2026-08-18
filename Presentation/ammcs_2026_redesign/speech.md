## Slide 1: Towards Validity-Weighted Attenuation of Affective Noise in Student Evaluations of Teaching

Title slide.

Full framing: an auditable aspect-based sentiment analysis framework that adjusts SET
ratings by down-weighting construct-irrelevant emotion. Built and evaluated on 17,127
RateMyProfessors reviews covering 1,029 professors.

## Slide 2: Slide 2

The problem, as a mock-up.

A RateMyProfessors profile with the overall score replaced by a question mark — "Overall
Ratings Based on a Biased System" — and a rating distribution showing the U-shape that
informal SET produces: a wall of 5s, a wall of 1s, and comparatively little in between.
The mock statistics underneath ("100% chance of it staying here for a long time",
"1.0 degree of fairness") are the joke, but the serious point is the question mark.

That number is what students actually act on when choosing courses. We do not know what
it measures. Everything in this talk is an attempt to make it mean something.

## Slide 3: Slide 3

Real review #1 — Quality 3.0, Difficulty 5.0, October 2008.

"dude is huge and i mean huge and is a rude guy but he knows alot about politics"

Walk the audience through it clause by clause, because this review comes back later as the
full worked example:
  - "dude is huge" — off-topic, physical appearance
  - "i mean huge" — off-topic, emphasis on the same
  - "is a rude guy" — off-topic, and emotionally charged (anger 0.567)
  - "he knows alot about politics" — the only pedagogical clause in the review

Three of four clauses have nothing to do with teaching, and the one that does is positive.
Yet the rating is a 3.0. That gap is the entire thesis in one review.

## Slide 4: Slide 4

Real review #2 — Quality 2.5, Difficulty 4.0, August 2011.

A long complaint about the instructor's voice, compared to Mrs. Doubtfire and Julia Child,
with "makes it hard to focus and i think she does it on purpose."

Two things worth naming:

First, this is almost entirely construct-irrelevant. Vocal quality is not instruction.
Yet the student presents it as decisive — "you need the facts, don't take her."

Second, note the last line: "I even got a B and i'm sayin this!" The student
pre-emptively defends against the grade-retaliation explanation, which tells you they know
it is the obvious objection. Their own report is that performance was fine and the rating
is still 2.5.

## Slide 5: Slide 5

Real review #3 — Quality 5.0, Difficulty 3.0, August 2004.

"BIg up to the selektah massive inside! Rinse out Prof. [name] propa...gunshots! boh! boh!
maximum Reeespect...."

This one is the counterpoint, and it is why deletion-based approaches fail. There is no
pedagogical content here at all — it is pure enthusiasm in dancehall idiom. A filter would
throw it out.

But it is not meaningless. It carries genuine positive affect toward the instructor. The
student is communicating something real; it just is not information about teaching.

Down-weighting handles this correctly: keep the review, keep the student's voice, reduce
the weight of the off-topic emotion. Deleting it discards a real person's real response.

## Slide 6: What are we actually measuring?

Section opener — the validity question.

The whole talk hangs off this: a SET score is a number, but it is not obvious what
construct that number measures. Everything that follows is an attempt to answer it
computationally.

## Slide 7: Scores averaged across an ill-defined assortment of items offer no basis for knowing what is being measured.

Marsh & Roche, American Psychologist, 1997, p. 1187.

The canonical statement of the problem. If the items being averaged are not a coherent
set, the average has no defined referent — you cannot say what the score measures. This
applies with more force to RMP than to formal instruments, because RMP imposes no item
structure at all.

The three reviews shown alongside are the ones just walked through — physical appearance
at 3.0, vocal quality at 2.5, dancehall enthusiasm at 5.0. Marsh & Roche were writing
about formal instruments with defined items. These are what the same critique looks like
with no items at all.

## Slide 8: Wongsurawat

Wongsurawat (2011).

Coins the "white noise" framing: pedagogically irrelevant content in student comments is
a source of measurement error, and comments that correlate poorly with teaching quality
should be discounted. Note that the proposed remedy is discounting — this is the direct
ancestor of the down-weighting approach taken here, though Wongsurawat does not build a
mechanism for it.

## Slide 9: Schiekirka

Schiekirka & Raupach (2015).

A systematic review of confounders in medical-education SET. Identifies three families:
student characteristics, student performance level, and features of the evaluation
process itself. Important because these are *systematic* confounders — they bias in a
consistent direction, so they do not average out across respondents.

## Slide 10: Li et al. (2025) — emotional interaction with the instructor leads students to overlook actual teaching quality

Li et al. (2025).

Qualitative work showing that students' emotional and relational response to an
instructor leads them to overlook actual teaching quality when rating. This is the
affective-noise mechanism specifically, and it is the one this framework targets.

## Slide 11: Three literatures, one finding

Three independent literatures converge on one finding.

Student ratings respond to content that has nothing to do with teaching — irrelevant
commentary (Wongsurawat), situational confounders (Schiekirka & Raupach), and emotional
response to the instructor (Li et al.).

The key point is the second line: these influences are systematic, not random. That
matters because it means averaging across many students does not remove them. Random
error shrinks with n; systematic bias does not. This is precisely why "just collect more
reviews" is not a solution.

And on RateMyProfessors, nothing constrains what students write — no item structure, no
moderation, no prompt. So the contamination ceiling is higher here than on any formal
instrument.

## Slide 12: Possible Solutions

Three families of response to the contamination problem.

1. Constrain the instrument — narrow, targeted items. Removes noise by construction.
   Cost: loses the expressiveness that makes open-ended feedback worth collecting, and
   cannot be applied retroactively to existing data.

2. Discard bad reviews — filter "low quality" comments. Removes noise by exclusion.
   Cost: discards signal along with noise, and requires someone to decide what counts as
   "bad" — an unaccountable judgment call.

3. Down-weight by content — keep every review, reduce the influence of irrelevant
   content. Attenuates noise while aiming to preserve signal. Bounded, auditable, and
   contextual to each individual review.

This talk takes option 3.

## Slide 13: Down-weighting is the principled choice

Why down-weighting rather than deletion, in three citations.

Cronbach (1951), classical reliability theory: measurement quality improves by reducing
error variance, not by removing observations.

Huber (1964), robust estimation: bounded-influence weighting yields more stable and less
biased estimates than deletion. The framing to emphasise — discarding an observation is
simply assigning it a weight of zero. It is the crudest possible point on a continuum we
otherwise have full access to. Once you see deletion as a degenerate case of weighting,
the choice to weight continuously is not exotic, it is the general case.

Marsh & Roche (1997): corrections that ignore valid variance risk "throwing the validity
baby out with the bias bathwater." This is the conservative-correction principle that the
mean |Δ| of 0.207 later reflects.

## Slide 14: The corpus

The corpus.

17,127 RateMyProfessors reviews across 1,029 professors, from the open-source dataset
released by He (2020). Each record is a 1–5 rating plus free text.

Mean review length is 40.1 words (SD 20.3) — these are short, informal, and unstructured.
That length matters downstream: short reviews give few clauses, which makes clause-level
aggregation noisier and makes a single off-topic clause proportionally influential.

Ratings are negatively skewed, with 5-star reviews dominating. This biases the regression
model toward the top of the scale and limits generalization at the low end — it comes
back in Limitations.

Ethics point, worth stating explicitly: RMP prohibits scraping. Permission was requested
and not granted. No data was collected directly from the site — everything here is from
the previously published open dataset.

## Slide 15: Research Questions

The three research questions, in full:

RQ1 — How does emotional content in pedagogical comments contribute to SET ratings?

RQ2 — To what extent does emotional content in pedagogically irrelevant comments
contribute to SET ratings?

RQ3 — Can emotional attenuation of irrelevant comments mitigate affective noise while
preserving pedagogical signal?

RQ1 and RQ2 are descriptive — they establish that both signal and noise are present and
measurable. RQ3 is the interventional one, and it is the actual contribution.

## Slide 16: Slide 16

Pipeline stage 0 — data.

RateMyProfessor dataset → data cleaning → individual student reviews, each a numerical
rating paired with free text.

The example review in the diagram is a good one to read out, because it is the normal
case rather than an extreme: "[Instructor] knows his material and could make it very
interesting. However there is no room for conversation...straight note-taking class. If
you like to write this is the class for you. It's all essay and memorization! Good Luck!"

That is mixed, multi-topic, and mostly pedagogical — exactly the kind of review the
framework should barely touch.

## Slide 17: Slide 17

Pipeline stage 1 — Aspect-Term Categorization and the density metric.

Every clause is sorted into one of four buckets: Instructional Effectiveness, Fairness,
Workload, or Miscellaneous. The diagram then splits the flow in two — Miscellaneous
content on one path, pedagogical content on the other — and recombines them into a single
scalar: the pedagogical content density metric, bounded 0 to 1.

The reason for the split is that the two paths get treated differently downstream. The
pedagogical side passes through untouched. Only the Miscellaneous side gets attenuated.

Everything after this point depends on that categorization being roughly right, which is
the cascade concern raised in Limitations.

## Slide 18: Slide 18

Pipeline stage 2 — the emotion model.

A multi-label RoBERTa GoEmotions model, pulled from Hugging Face. Multi-label matters:
a clause can register admiration and annoyance simultaneously, which short informal
reviews frequently do.

## Slide 19: Slide 19

Pipeline stage 2 continued — emotions per topic, not per review.

This is the design decision that everything else rests on. Emotion is not extracted for
the review as a whole; it is extracted separately for each topic within the review.

That is what makes the intervention possible. If you only had one sentiment score per
review, there would be nothing to attenuate selectively — you could only dampen the whole
thing. Because emotion is indexed by topic, we can reach in and down-weight the emotion
attached to off-topic content while leaving pedagogical emotion completely untouched.

The comparison argument on the RQ3 Cont. slide is about exactly this.

## Slide 20: Slide 20

Pipeline stage 3 — regression.

A CatBoost model is trained to predict the numerical rating from the topic-indexed
emotion matrix. Four topics, each with its own emotion profile, mapping to a single star
rating.

The model is not the contribution — it is the instrument. Its job is to give us a
defensible estimate of how much each block of emotion contributed to the rating, so that
we can remove a specific block and measure the difference.

That is also why interpretability at this stage matters more than raw accuracy.

## Slide 21: Slide 21

Pipeline stage 4 — the full attenuation architecture. This is the money diagram;
spend time here.

Two feature vectors go into the same trained CatBoost model:
  - Top: baseline emotions, untouched.
  - Bottom: identical, except Miscellaneous emotions have been down-weighted according
    to the pedagogical density metric. Note the red down-arrow on Misc, and that
    Instructional Effectiveness, Fairness, and Workload are visibly unchanged.

The model is the same model in both cases. Nothing is retrained. That is what makes the
difference between the two predictions attributable to the intervention and nothing else.

The formula on the right is the whole method:

    ŷ_adjusted = y_raw + (ŷ_attenuated − ŷ_baseline)

Read it out loud in words: take the student's actual rating, and add the amount the model
says the rating would have moved if the off-topic emotion had been proportionally quieter.

The star rows make the point visually — raw 4 of 5 becomes adjusted 3 of 5. And note what
is being kept: y_raw is the starting point. The student's judgment is never replaced, only
corrected by an amount we can point at and defend.

## Slide 22: In Greater Detail

Pipeline roadmap — four stages, each covered in turn:

1. ATC (Aspect-Term Categorization) — sort every clause into a topic.
2. Sentiment extraction — a 28-dimensional emotion vector per clause.
3. CatBoost modeling — predict the rating from topic-level emotion.
4. Validity-weighted attenuation and rating adjustment — the intervention itself.

## Slide 23: ATC

Aspect-Term Categorization, in detail.

Review clauses are embedded using all-mpnet-base-v2. Written descriptions of each
category are embedded in the same space. Cosine similarity then measures the semantic
distance between each clause and each category description.

Each clause is assigned to the highest-similarity category, but only if that similarity
exceeds 0.25. Otherwise it falls through to Miscellaneous. So Miscellaneous is both a
real category and the residual bucket — anything the taxonomy does not recognise as
pedagogical ends up there, which is exactly the behaviour we want for a noise proxy.

The four categories: Miscellaneous, Instructional Effectiveness, Workload, Fairness.

This is zero-shot — no labelled training data for categorization. That keeps it portable
to other domains by swapping the category descriptions, and it is why accuracy is
"acceptable rather than excellent" (see Limitations).

## Slide 24: Miscellaneous

Miscellaneous Density, D_misc.

The proportion of the overall review directed toward the Miscellaneous category —
computed over word counts. It represents how on-topic a review is.

D_misc = 1.0 means the review is entirely off-topic. D_misc = 0 means fully on-topic.

This single scalar is the load-bearing quantity in the whole framework: it is what drives
the attenuation weight ζ later on. Worth flagging now that it is a proxy — word share
aimed at a residual category — not a direct measurement of noise. That distinction
returns in both Discussion and Limitations.

Distribution across the corpus is heavily right-skewed with a median of 0.11, but with a
non-trivial tail of reviews carrying substantial off-topic density.

## Slide 25: Slide 25

ATC architecture in detail.

Two things get embedded into the same vector space by all-mpnet-base-v2: written
descriptions of each category (Instructional Effectiveness, Fairness & Grading, Workload
& Difficulty), and the individual review clauses.

Cosine similarity between a clause embedding and each category embedding produces a
similarity vector [s₁, s₂, s₃]. The highest wins, provided it clears 0.25. Below that
threshold, the clause falls through to Miscellaneous.

Two points worth making from this diagram:

The category descriptions are the only domain-specific component. Swap them and the
framework moves to another domain — this is the modularity claim in the practical
implications.

And note there are three descriptions but four categories. Miscellaneous has no
description of its own; it is the residual, defined by failure to match anything else.
That is deliberate — you cannot enumerate everything students might write about, so you
define the pedagogical space and treat the complement as noise.

## Slide 26: Sentiment Extraction

Sentiment extraction.

Categorized clauses are fed individually into roberta-base-go_emotions — a model trained
from roberta-base on the GoEmotions dataset (Reddit comments) for multi-label emotion
classification.

Output is a 28-dimensional emotional probability vector per clause. Multi-label, not
single-label, so a clause can carry admiration and disappointment simultaneously — which
short informal reviews frequently do.

An INT8 quantized ONNX model was used for throughput. Note the trade-off: quantization
costs some accuracy, and the training domain (Reddit) is not the deployment domain
(student reviews), which limits performance on sarcasm and academic idiom. Both appear in
Limitations.

## Slide 27: Feature Aggregation per Review

Feature aggregation — the problem and the solution.

The problem: a single review can contain clauses from several different categories, and
each clause carries its own 27-feature emotion vector. How do you get to one feature
vector per review?

The solution, in three steps:
- Combine all categories into one vector across the review's clauses.
- Average the emotional contributions directed toward the same category.
- Impute zeros where a category was never mentioned.

That last step is why the feature matrix is sparse — most reviews do not touch all four
categories — and it is why CatBoost was chosen, since it handles sparsity well.

The averaging step is a real information loss: a review with one furious Workload clause
and one mild one produces the same average as two moderate ones. Flagged in Limitations
as a place where nuance is lost, particularly in short reviews with mixed sentiment.

## Slide 28: Feature Aggregation Cont.

The arithmetic: 27 emotion features × 4 categories = 108, plus the four
density terms (D_misc, D_eff, D_work, D_fair) = 112 features per review.

D_misc is Miscellaneous density, D_eff is Instructional Effectiveness density, and so on
for Workload and Fairness. The densities are what let the model condition on how on-topic
a review is, not just what emotions it contains.

## Slide 29: CatBoost

CatBoost modeling.

CatBoost is a gradient-boosted tree library that handles categorical and numerical data
for regression. It was chosen because it is highly effective on sparse data — remember
all those imputed zeros from the aggregation step — and on non-linear relationships.

Ratings are modeled as a function of category-specific emotional features plus the four
densities.

Validation design: professor-level grouped split with 5-fold cross-validation. Grouping
by professor matters — without it, multiple reviews of the same instructor would leak
across the train/test boundary and inflate performance.

The trained model is saved, and baseline predictions are preserved. That second point is
essential to the attenuation step: the adjustment is defined as the difference between
the baseline prediction and the attenuated prediction, so the baseline has to be held
fixed.

## Slide 30: Other non-

Model comparison. CatBoost was not assumed — it was selected.

Ordinal Regression   MAE 0.9509 · Spearman ρ 0.5414 · R² 0.0794
Linear Regression    MAE 0.7940 · Spearman ρ 0.6875 · R² 0.5266
Random Forest        MAE 0.6938 · Spearman ρ 0.7289 · R² 0.6217
XGBoost              MAE 0.6710 · Spearman ρ 0.7329 · R² 0.5638

CatBoost wins on the combination, reaching ρ = 0.7355 and R² = 0.6140. Ordinal regression
performing worst is the interesting result — despite ratings being ordinal by nature, the
relationship between emotion features and rating is non-linear enough that a linear
ordinal model cannot capture it.

## Slide 31: Validity-Weighted Attenuation

The attenuation mechanism itself.

Miscellaneous emotions are down-weighted by ζ (zeta), where ζ = 1 − D_misc^s. The exponent s controls the
non-linearity of ζ. As D_misc increases, ζ decreases — so the more off-topic a review is,
the harder its off-topic emotions are suppressed.

The down-weighting is proportional to D_misc, which means it is contextual to each
individual review rather than a blanket rule. All other features are preserved untouched:
pedagogical emotions and the density terms pass through unchanged. Only E_misc is
modified.

Note for questions: s does not have a unique optimum. Several values across the search
range produce near-equivalent loss, and resampling the tuning professors selects values
between 0.23 and 0.94. Downstream adjustments are highly stable across that range
(Pearson r > 0.96 between Δ vectors), so results do not depend materially on the value —
but the exponent is weakly identified and I would rather say so than be asked.

## Slide 32: Validity-Weighted Attenuation Cont.

Completing the adjustment.

The attenuated feature vector goes back into the same fixed CatBoost model, which
produces a new predicted rating. Take the difference between the attenuated prediction and
the baseline prediction. That difference is the model-estimated contribution of the
off-topic emotion, and it is added to the original student rating (equivalently: the model-estimated off-topic contribution is removed).

Two design properties worth stressing:

First, the model is held fixed. Nothing is retrained. The only thing that changes between
the two predictions is the E_misc block, so the difference is attributable to that
intervention and nothing else.

Second, the raw student rating is preserved throughout — the adjustment is added to it,
not substituted for it. The student's evaluative intent is never discarded, only
corrected by an amount we can point at and justify.

## Slide 33: Slide 33

Worked example — Review #8113. This is the review from the opening: "dude is huge
and i mean huge and is a rude guy but he knows alot about politics."

Section 1, clause by clause:
  "dude is huge"                  → Misc, sim 0.030, admiration 0.044
  "i mean huge"                   → Misc, sim −0.010, approval 0.018
  "is a rude guy"                 → Misc, sim 0.200, anger 0.567, annoyance 0.361
  "he knows alot about politics"  → Instr. Effectiveness, sim 0.270, approval 0.293

Notice the third clause carries by far the strongest emotion in the review — anger at
0.567 — and it is aimed at the instructor as a person, not at their teaching.

Section 2 — the intervention. Instructional Effectiveness is byte-for-byte identical
before and after: approval 0.293, admiration 0.031, and so on. Only the Miscellaneous row
changes, shown in red: anger 0.192 → 0.056, annoyance 0.129 → 0.038.

Section 3 — the arithmetic. Three of four clauses are Miscellaneous, so D_misc = 0.670,
which gives ζ = 0.291 — roughly a 71% reduction in off-topic emotion. Baseline prediction
2.506, attenuated prediction 3.159, so Δ = +0.653. The student rated 3.0; adjusted is
3.653.

The interpretation to say out loud: the model's read is that this professor was marked
down substantially for being rude and physically conspicuous, not for their teaching —
and the one thing the student said about the teaching was positive. This is what an
auditable adjustment looks like. Every number here is inspectable and every step is
attributable.

## Slide 34: Results

Section opener — Results.

## Slide 35: Slide 35

Distribution of Miscellaneous content density across all 17,127 reviews.
Mean 0.22, median 0.11.

Three features to point at:

The huge spike at zero — nearly 7,000 reviews are entirely on-topic. Those receive
essentially no adjustment, which is the correct behaviour and worth stressing: the
framework is not rewriting the corpus.

The long flat tail out to 0.8 — a substantial minority of reviews carry meaningful
off-topic content.

And the second spike at exactly 1.0 — roughly 1,000 reviews are entirely off-topic. This
is the collapse case from Limitations: at D_misc = 1 the emotions are fully down-weighted,
so those reviews all produce identical feature vectors and the model returns the same
prediction for all of them. It is a visible artifact, not a hidden one, which is why it is
worth showing this chart rather than just quoting the median.

## Slide 36: Slide 36

Clause topics versus rating — raw clause counts.

The headline is the 1-star column. Miscellaneous is 2,882 clauses against Instructional
Effectiveness at 2,274 — that is the ~27% figure from the RQ2 slide, and it means that in
the angriest reviews, the single most common thing students talk about is not teaching.

Contrast the 5-star column: Instructional Effectiveness 11,079, nearly double
Miscellaneous at 5,785. When students are happy, they talk about the instruction.

Fairness is the thin row throughout, but look at its shape — 936 clauses at 1-star,
falling to 264 at 2.5, then climbing back to 813 at 5-star. It is the most bimodal topic
in the corpus: students raise fairness when they feel wronged or when they feel
exceptionally well treated, and rarely otherwise.

Caveat if asked: these are raw counts, and the corpus is 5-star heavy, so column totals
are not comparable in absolute terms. The within-column proportions are the meaningful
comparison.

## Slide 37: Slide 37

5-Star clauses: emotion heatmap. Note the single darkest cell in the grid.

Admiration toward Instructional Effectiveness at 0.47 dominates everything else on the
slide — nothing else exceeds 0.19. High ratings are driven by concentrated positive affect
aimed squarely at teaching.

But look at the Miscellaneous row: admiration 0.28, approval 0.12, love 0.07. That is
substantial positive emotion aimed at things that are not teaching. So even in the
best-case reviews, where signal-to-noise is most favourable, the absolute quantity of
off-topic affect is high. Favourable ratio, not absent noise.

Compare with the next slide — the structural difference between the two ends of the scale
is the point.

## Slide 38: Slide 38

1-Star clauses: emotion heatmap. Put this beside the 5-star heatmap.

Where 5-star had one dominant cell at 0.47, 1-star has no peak at all — the maximum
anywhere is 0.15, and negative emotion is spread evenly across every topic including
Miscellaneous. Annoyance and disapproval sit at 0.11 to 0.15 across the board.

So the two ends of the scale are structurally different. High ratings are concentrated
praise for teaching. Low ratings are diffuse dissatisfaction with everything.

Two details worth flagging. Fairness carries the single highest negative value on the
slide — annoyance at 0.15 — which supports grading equity as the sharpest concern among
dissatisfied students. And the Miscellaneous row is fully lit up: annoyance 0.11,
disapproval 0.11, anger 0.05. Off-topic negativity is a real component of low ratings.

This is the asymmetry that makes proportional attenuation the right tool. There is no
single emotion or topic you could target with a fixed rule.

## Slide 39: Slide 39

SHAP beeswarm — baseline model, before any attenuation. This is the RQ1 and RQ2
evidence in one chart.

Ranked by importance:
  1. Positive Instructional Effectiveness — the widest spread, pushing to +0.09
  2. Negative Instructional Effectiveness — reaching −0.15
  3. Negative Miscellaneous
  4. Negative Workload
  5. Positive Miscellaneous
  6. Negative Fairness
  7. Positive Workload
  8. Positive Fairness

Two readings, and be explicit about which is which:

By individual feature — Negative Miscellaneous is third, above both polarities of Fairness
and Workload. Off-topic negativity outweighs how students feel about their grades and
their workload.

By category, summing polarities — Miscellaneous is second overall behind Instructional
Effectiveness, with a mean |SHAP| of 0.671. Same data, different aggregation, both numbers
correct.

Also worth noting that Positive Miscellaneous is fifth. Off-topic content pushes ratings
in both directions — it is not simply a penalty term.

## Slide 40: Slide 40

Frequency distribution of attenuation Δs across all reviews. Mean Δ = +0.0404.

The shape is the argument. It is sharply peaked at zero — the overwhelming majority of
reviews barely move, because the overwhelming majority are mostly on-topic. This is a
targeted correction, not a global rescaling.

The mean is slightly positive at +0.04, which reflects that off-topic emotion in this
corpus skews negative — so removing it more often nudges ratings up than down. Do not
overstate that; it is a small aggregate effect.

Then the tails. Out to +2.6 on the right and −1.4 on the left sit the reviews with high
off-topic density and strongly polarized off-topic emotion. Those are the cases the
framework exists for.

Note also that mean Δ (+0.04) and mean |Δ| (0.207) are different quantities — the signed
mean nearly cancels, the absolute mean does not. Quote whichever answers the question
being asked, but do not mix them up.

## Slide 41: Slide 41

Professor-level rating distributions, raw versus adjusted, as kernel density
estimates.

The two curves sit almost on top of each other and the means are visually
indistinguishable. Say what that means plainly: at the aggregate level, almost nothing
happens.

The visible difference is a slight compression — the adjusted curve peaks marginally
higher around 4.2 and has slightly thinner tails at both ends.

This is the answer to "does this just move everyone's scores around?" No. The population
distribution is preserved. The framework is not inflating or deflating ratings globally;
it is redistributing at the individual level where off-topic content is concentrated.

If someone objects that this makes the method look inconsequential — that is precisely the
conservative-correction behaviour Marsh & Roche argue for, and the next slide shows where
the action actually is.

## Slide 42: Slide 42

The twenty professors whose average ratings moved most, positive and negative.

Range is roughly +0.66 down to −0.94. So while the population distribution barely moves,
individual instructors can shift by close to a full point.

This is where the method matters, and it is also where the stakes are. A 0.9-point
correction to an instructor's average is consequential if anyone acts on it — which is
exactly why the audit trail from the worked example is not optional. Every one of these
professor-level shifts decomposes into individual review adjustments, each of which
decomposes into specific clauses and emotions.

Be careful with the framing: these are the professors whose reviews contained the most
off-topic emotional content. That is not the same as saying these are the professors most
unfairly rated — that claim would require the ground truth we do not have.

Note the asymmetry: the largest downward correction (−0.94) exceeds the largest upward one
(+0.66).

## Slide 43: Validation

Section opener — Validation.

## Slide 44: Slide 44

Mean |SHAP| contribution by category, baseline versus attenuated. The raw numbers
behind the percentage-change chart.

  Instructional Effectiveness  1.109 → 1.131
  Fairness                     0.188 → 0.193
  Workload                     0.461 → 0.473
  Miscellaneous                0.674 → 0.601

Miscellaneous falls; all three pedagogical categories rise. That is the direction we
wanted, and it is the core internal-validation result.

Two honest observations. First, note that Miscellaneous at 0.674 baseline is the second
largest bar on the chart — larger than Workload and Fairness combined. That is the RQ2
finding in its starkest form. Second, even after attenuation Miscellaneous is still 0.601,
so this is a reduction in influence, not an elimination of it.

Mechanical caveat if pressed: the pedagogical increases are partly redistribution — total
importance is roughly conserved, so suppressing one category necessarily raises the
others' relative share. The result to lean on is the direction and the asymmetry of
magnitude, not the increase in isolation.

## Slide 45: Slide 45

The same result as percentage change: Miscellaneous −10.8%, Fairness +2.8%,
Workload +2.6%, Instructional Effectiveness +2.0%.

One large negative, three modest positives. The asymmetry is the point — this is not a
uniform rescaling, it is importance moving off one specific category and being absorbed
across the other three.

Worth noting that Instructional Effectiveness gains the least in percentage terms despite
being by far the largest category. It was already dominant; there was less headroom. The
proportionally largest gains go to Fairness and Workload, the two categories that were
being most crowded out by off-topic content.

## Slide 46: Slide 46

Weighted percentage change in correlation magnitude after adjustment — Pearson and
Spearman shown separately.

  Instructional Effectiveness  +1.2% Pearson, +0.9% Spearman
  Fairness                     +1.2% Pearson, +0.4% Spearman
  Workload                     +1.0% Pearson, +0.7% Spearman
  Miscellaneous                −7.8% Pearson, −10.8% Spearman

This is the cleanest internal result in the deck, because both directions move
simultaneously. Adjusted ratings correlate more strongly with pedagogical emotion and
less strongly with off-topic emotion. A method that was simply adding noise would degrade
both; a method that was simply shrinking everything would degrade both.

Note that Miscellaneous drops harder on Spearman (−10.8%) than Pearson (−7.8%) — the
rank-order relationship weakens even more than the linear one, which is the more
conservative of the two measures moving in the right direction.

Magnitudes are small. State that rather than letting someone else point it out — this is
consistent with a fine-tuning mechanism, and it is why the paper's language is "tentative
evidence" rather than a claim of validity.

## Slide 47: ∆+  Versus

Attenuation Δs against Miscellaneous density, split by direction, with point shading
for emotional intensity.

Left panel, positive Δs (rating increased), shaded by negative emotional intensity:
  vs D_misc — Pearson 0.6956, Spearman 0.6218
  vs Neg. E_misc — Pearson 0.3600, Spearman 0.4185

Right panel, negative Δs (rating decreased), shaded by positive emotional intensity:
  vs D_misc — Pearson −0.6966, Spearman −0.5607
  vs Pos. E_misc — Pearson −0.2258, Spearman −0.1063

Read the scatters, not just the numbers. Both show a clear linear trend, and both show
the variance fanning out as density increases — at low D_misc the adjustments are tightly
clustered near zero; at high D_misc they range widely. Density sets the ceiling on how
much a review can move; emotional intensity determines where within that range it lands.
That is the mechanism behaving as designed.

The vertical stripe at exactly 1.0 in both panels is the collapse case — fully off-topic
reviews, spread across the full range of Δ.

Now the caveat, and volunteer it rather than waiting: the strong D_misc correlations are
partly true by construction, since D_misc drives ζ which drives Δ. What they establish is
that the mechanism is systematic rather than arbitrary — not that it has found real noise.
The Pearson–Spearman gap is a small tail of extreme reviews inflating the linear fit;
Spearman is the conservative reading.

The asymmetry between panels is unexplained. The upward side tracks emotional intensity
noticeably better (0.36/0.42) than the downward side (−0.23/−0.11). Flagged in the paper
as warranting further investigation — say so if asked rather than improvising a reason.

## Slide 48: External Expert Validation

External expert validation.

The full question: does the framework produce relative differences in adjustments between
pairs of reviews that agree with a senior faculty expert's assessment of those same pairs?

Results by condition:
  45 pairs — 40 correct, 3 unsure — accuracy 0.889, p < 0.001
  29 pairs — 22 correct, 1 unsure — accuracy 0.759, p < 0.005

Why pairwise rather than absolute: there is no ground truth for how much a given rating
*should* move, so asking an expert to validate a magnitude is unanswerable. Asking which
of two reviews deserves the larger correction is answerable. The cost of that design is
that it tests direction only, never magnitude — which is why it appears in Limitations.

Single annotator. State it before someone asks.

## Slide 49: Discussion

Section opener — Discussion.

## Slide 50: Reminder of RQs

Reminder of the three research questions before answering them in turn.

RQ1 — How does emotional content in pedagogical comments contribute to SET ratings?
RQ2 — To what extent does emotional content in pedagogically irrelevant comments
contribute to SET ratings?
RQ3 — Can emotional attenuation of irrelevant comments mitigate affective noise while
preserving pedagogical signal?

## Slide 51: RQ1

RQ1 — answered.

There is a clear relationship between pedagogical feedback and numerical ratings, and
Instructional Effectiveness dominates on every measure:

- Most frequent pedagogical topic.
- Most elaborated — 1.92 clauses per review on average, the highest of any category.
  Students write more about it when they write about it at all.
- Strongest emotional intensities when mentioned.
- Highest mean SHAP value of any topic.

In the baseline SHAP ranking, Positive Instructional Effectiveness is the single largest
driver of predicted ratings, with Negative Instructional Effectiveness second.

Workload is the second most frequent pedagogical topic but contributes more variably.
Fairness is less frequent overall but behaves distinctively in low-rating contexts.

So: emotional response to pedagogical topics — Instructional Effectiveness above all — is
a primary systematic driver of rating variation. That answers RQ1.

## Slide 52: RQ2

RQ2 — answered.

Two rankings here, and they are different numbers for different things — be explicit or
the audience will think one is a mistake:

  - As a *category*, Miscellaneous ranks 2nd overall, behind only Instructional
    Effectiveness (mean SHAP 0.671 for E_misc).
  - As an individual *feature*, Negative Miscellaneous ranks 3rd, behind Positive and
    Negative Instructional Effectiveness — and above both polarities of Fairness and
    Workload. Positive Miscellaneous ranks 5th, so it pushes in both directions.

Miscellaneous is also simply everywhere. It is the most frequent clause category in
1-star reviews, occurring roughly 27% more often than the next most common topic there.
D_misc across the corpus has a median of 0.11 but a heavy right tail — off-topic content
is a recurring structural feature of informal SET, not an occasional aberration.

And it contaminates the entire scale, in two different ways:
  - High ratings: large absolute off-topic noise, but the pedagogical signal is strong
    enough that signal-to-noise stays favourable.
  - Low ratings: smaller absolute emotional contributions overall, but Miscellaneous
    makes up a proportionally larger share of what is there.

Either way there is no safe region of the scale. This aligns with Messick's (1995)
construct-irrelevant variance, and with Dowell & Neal (1983) and Wongsurawat (2011) on
SET capturing satisfaction rather than instruction.

## Slide 53: RQ3

RQ3 — answered, tentatively.

First, the model is worth trusting: ρ = 0.7355, R² = 0.6140. Ratings are not arbitrary;
they are a predictable function of topic-level emotion.

Importance shift after attenuation — SHAP-based feature importance moves off Miscellaneous
(−10.8%) and onto the pedagogical categories: Instructional Effectiveness +2.0%,
Fairness +2.7%, Workload +2.6%. When the construct-irrelevant signal is suppressed, the
model leans harder on pedagogy.

Statistical separation — attenuated ratings maintain or strengthen correlations with
pedagogical emotion (E_eff, E_fair, E_work) while reducing correlation with E_misc. Both
directions move the right way at once, which is the result that suggests the mechanism is
doing what it claims.

Magnitude — mean absolute rating change is 0.2072 points, with a tail of larger targeted
corrections for reviews combining high density with intense off-topic polarization. At the
professor level the distribution shape is largely preserved. This is fine-tuning, not
wholesale rewriting — the conservative correction Marsh & Roche argue for.

Coherence — Δ⁺/Δ⁻ against D_misc gives r = 0.696 / −0.697. Say the caveat out loud rather
than waiting to be caught: this is partly true by construction, because D_misc drives ζ
directly. It demonstrates the mechanism is systematic, not that it has found real noise.
Spearman is lower (0.622 / −0.561) because a small tail of extreme reviews inflates the
linear fit.

Plus preliminary agreement with expert judgment. Together this addresses RQ3 — with
"tentative" doing real work in that sentence.

## Slide 54: RQ3 Cont.

The design argument, not the results argument.

Theory into mechanism: Messick (1995) supplies the construct-irrelevant variance framing,
Huber (1964) justifies bounded-influence weighting over deletion, Cronbach (1951)
justifies reducing error variance rather than removing observations. Each is a concrete
design decision in the pipeline, not a decorative citation.

Interpretability as a constraint, not a feature: every adjustment traces back through
clause → category → emotion → density. The model is held fixed and a targeted intervention
is applied, so the prediction difference is attributable. The worked examples in the paper
show a full trace for individual reviews.

The comparison makes the case. With aggregate sentiment instead of topic-level
extraction you would lose three things: predictive accuracy, proportional scaling (you
could only apply a blanket dampening factor), and — most importantly — the ability to say
*which* emotion drove an adjustment. Swapping in LLMs or deep networks might buy marginal
component-level performance at the cost of the audit trail. In a consequential evaluation
setting that is the wrong trade.

## Slide 55: Practical Implications

Practical implications.

For informal platforms like RMP: a mechanism to make displayed ratings more trustworthy.
Adjusted scores could be a better signal for students choosing courses, and topic-level
breakdowns would let a reader distinguish a Fairness complaint from a Workload complaint
instead of collapsing both into one number.

For institutions: a direction for validity-aware processing of formal SET data — with the
caveat that this is proof-of-concept and would need substantially more validation before
any consequential use.

For faculty development: the topic-level analysis is diagnostic. Instructional
Effectiveness dominating suggests where instructional investment pays off; Fairness being
over-represented in low-rating reviews flags grading and equitable treatment as a
high-impact concern.

For other domains: the category descriptions are the only domain-specific component, so
the framework transfers by rewriting them — healthcare satisfaction surveys, product
reviews, employee performance feedback (Pelaez et al. 2026; Lim & Tucker 2017;
Gaye et al. 2021).

## Slide 56: Limitations

The joke slide — then take the limitations seriously.

Deliver it, get the laugh, then land the turn: the fact that we can enumerate the failure
modes this precisely is the point of building an interpretable system rather than a
black box.

## Slide 57: Limitations

Limitations, part one.

No ground truth for teaching quality — the fundamental one. Internal consistency,
improved signal-to-noise, and expert alignment are all indirect evidence. None of them
prove adjusted ratings better reflect true teaching quality. Establishing criterion
validity would need external benchmarks — learning outcomes, peer evaluation, longitudinal
performance — none of which exist for RMP. So: a method for reducing noise, not a
definitive correction toward truth.

One platform, one corpus — RMP is anonymous, unmoderated, self-selected, and 5-star
skewed. Formal SET instruments differ in structure, administration, and respondent
motivation. Generalization is untested. Also: clause segmentation is imperfect, since
irregular punctuation and multi-clause sentences defeat the spaCy splitter.

Preliminary expert validation — a single annotator. Subjectivity enters, and the results
are contingent on one individual's judgment. Generalizability cannot be strongly claimed.

Direction, not magnitude — the pairwise design tests whether relative adjustments agree
with expert judgment. Large Δs align well; smaller differences are less reliably captured.
It says nothing about whether any specific adjustment is the right size.

Errors cascade — ATC accuracy feeds D_misc accuracy, which feeds Δ, which feeds final
adjustment validity. External validation only tested the final output under controlled
upstream conditions, so upstream error is not fully accounted for.

## Slide 58: Limitations Cont.

Limitations, part two — mostly component-level.

ATC is broad and single-label — informally defined categories, one label per clause even
when several apply. Multi-topic clauses get forced into one bucket. Acceptable for
zero-shot, but there is room.

RoBERTa-GoEmotions trained on Reddit — not on student reviews. Sarcasm and academic idiom
get misread, and sarcasm is common in low-rating SET text.

Collapse point at D_misc = 1 — when Miscellaneous is the only topic present, emotions are
fully down-weighted and different reviews produce identical feature vectors. The model
then returns the same attenuated rating for all of them.

Neutral-but-off-topic is invisible — the framework attenuates emotion. A review that is
entirely off-topic but emotionally flat has nothing to attenuate and passes through
untouched, despite being exactly the kind of content we would want to discount.

Just one flavour of noise — this addresses construct-irrelevant *emotional* content only.
It does not touch grading leniency, course difficulty, or demographic bias. Worth being
direct here: the dataset contained demographic information that was not used, so adjusted
scores may still carry whatever gender or racial inequities are present in the raw data.

Efficiency-first choices cap the ceiling — compact zero-shot ATC model, INT8 quantized
RoBERTa, lightweight regression. All chosen for throughput, all leaving performance on the
table.

Also, if asked about hyperparameters: results may be sensitive to empirically selected
thresholds throughout ATC, regression, and attenuation. The exponent s in particular is
weakly identified — resampling selects values from 0.23 to 0.94 — though downstream
adjustments stay stable across that range at r > 0.96.

## Slide 59: Conclusion

Section opener — Conclusion.

## Slide 60: Decompose → extract clause emotion → down-weight off-topic proportionally → re-predict → adjust

The whole pipeline in one line: decompose the review into clauses, extract
clause-level emotion, down-weight off-topic content proportionally to its density,
re-predict, and adjust the original rating by the difference.

Worth pausing on "proportionally" — that is the word carrying the argument from the
Huber slide. Nothing is deleted, nothing is zeroed except in the degenerate case, and the
student's rating survives as the starting point.

## Slide 61: Contributions

Three contributions.

Intervene, don't just detect — prior computational SET work is largely descriptive:
identify sentiment, characterise bias, report it. This framework acts on the rating. That
is the gap it fills.

Psychometric theory made computational — Messick's construct-irrelevant variance, Huber's
bounded-influence estimation, and Cronbach's error-variance framing translated into a
concrete mechanism rather than cited as background.

Every adjustment is auditable — each rating change traces to specific topic-level emotions
and a measured content density. An administrator can inspect why any individual review
moved, which is a precondition for use in any consequential setting (Doshi-Velez & Kim,
2017).

## Slide 62: Proof-of-concept noise reduction, not a validated measure of teaching quality.

The honest scoping statement — say this plainly rather than hedging.

What the evidence supports: proof-of-concept noise reduction. Feature importance moves off
construct-irrelevant content and onto pedagogy, correlations separate in the right
directions, and relative adjustments agree with expert judgment above chance.

What it does not support: that adjusted ratings are a validated measure of teaching
quality. Without ground truth that claim cannot be made, and I am not making it.

Possibly extendable to formal SET systems — with the emphasis on possibly, and only after
the validation work in the next slide.

## Slide 63: What’s Next?

Future work.

Formal SET corpora — structured prompts and standardized scales would likely lower the
Miscellaneous baseline and require recalibrating attenuation parameters. Multilingual
support would extend reach beyond English-language contexts.

Alternative stage implementations — better clause segmentation, RoBERTa fine-tuned on
student review text, smarter aggregation than simple averaging, richer non-affective
features so that emotionally neutral reviews remain distinguishable. Benchmarking against
LLM approaches to quantify what transparency actually costs in performance terms.

More robust attenuation — a density metric grounded in semantic relevance rather than word
share, fallback handling for the D_misc = 1 collapse, and extension to other CIV sources
including demographic bias.

Multiple experts — the single-annotator limitation is the cheapest one to fix.

An external criterion — peer evaluations, teaching portfolios, learning outcomes. Do
attenuated ratings correlate better with these than raw ratings do? That is the test that
would move this from noise reduction to validity improvement.

Fairness audits — verify the framework does not amplify existing inequities across
instructor demographics and disciplines.

## Slide 64: Validity concerns in informal SET can be addressed computationally

Closing line — deliver it and stop.

Validity concerns in large-scale informal SET data can be addressed computationally
without sacrificing interpretability and without discarding student voice. Both halves
matter: the deletion-based alternatives throw away real feedback, and the black-box
alternatives cannot explain themselves in a setting where explanation is a requirement.

## Slide 65: Acknowledgements

Acknowledgements — AMMCS participants and staff, Professor Somayeh Fatahi,
my father, the senior faculty experts who provided validation judgments, and the Laurier
Research Ethics Board.
