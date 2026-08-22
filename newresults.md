=== Stage 5: Attenuation ===
Loading model and data...
  Tuning s on 8,328 reviews from 823 training professors
  Running grid search for optimal s...
  Optimal s = 0.93  (loss = -1.4780)
  NOTE: tuned s = 0.93 differs from S_VALUE = 0.83. This run uses 0.93 throughout; update S_VALUE so later stages agree.
  Using s = 0.93
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\data\processed\weighted_emotions.csv
  Held-out reviews (misc subset): 2,052 of 10,380

  Total ratings attuned:        60.59%
  Ratings increased:            31.22%
  Ratings decreased:            29.37%
  Max |Δ|:                      2.5569
  Mean |Δ| (adjusted reviews):  0.2037
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\data\processed\attuned_ratings.csv
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\data\processed\attuned_ratings_full.csv
(absa) PS C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation> python -m src.validation              

=== Stage 6: Validation ===
  Warning: 3 pair(s) dropped — review_id not found in attuned data.
    review_id_1=14144  review_id_2=18846
    review_id_1=13330  review_id_2=678
    review_id_1=18844  review_id_2=7083
  Note: 4 pair(s) marked unsure — counted as incorrect.

====================================================
  EXPERT VALIDATION RESULTS
====================================================

  ────────────────────────────────────────────────
  Overall
  ────────────────────────────────────────────────
  Pairs evaluated : 77  (4 unsure → incorrect)
  Correct         : 62
  Accuracy        : 80.5%
  Binomial p-value (vs. chance = 0.5): 0.0000000

  ────────────────────────────────────────────────
  Coarse  (Difference in |Δ| ≥ 0.5)
  ────────────────────────────────────────────────
  Pairs evaluated : 45  (3 unsure → incorrect)
  Correct         : 40
  Accuracy        : 88.9%
  Binomial p-value (vs. chance = 0.5): 0.0000000

  ────────────────────────────────────────────────
  Fine    (0 ≤ Difference in |Δ| < 0.5)
  ────────────────────────────────────────────────
  Pairs evaluated : 32  (1 unsure → incorrect)
  Correct         : 22
  Accuracy        : 68.8%
  Binomial p-value (vs. chance = 0.5): 0.0250512

  Bins partition the pairs: 77 of 77 assigned.
(absa) PS C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation> python -m src.robustness

=== Stage 7: Robustness ===
Loading model and data...

  s values: [0.37, 0.62, 0.91, 0.93]   (pipeline uses S_VALUE = 0.93)
  Held-out misc reviews: 2,052

==================================================================
  tab:sensitivity-delta-agreement
==================================================================

 $s_a$  $s_b$  Pearson $r$  Spearman $\rho$  Mean $|\Delta_a - \Delta_b|$  Max $|\Delta_a - \Delta_b|$
0.3700 0.6200       0.9850           0.9239                        0.0564                       0.6234
0.3700 0.9100       0.9651           0.8159                        0.0851                       0.8907
0.3700 0.9300       0.9641           0.8102                        0.0862                       0.8960
0.6200 0.9100       0.9921           0.9114                        0.0394                       0.3933
0.6200 0.9300       0.9916           0.9051                        0.0408                       0.3986
0.9100 0.9300       0.9998           0.9941                        0.0043                       0.0726

==================================================================
  tab:sensitivity-modulators
==================================================================

   $s$  $\Delta^+$ Pearson $r$  $\Delta^+$ Spearman $\rho$  $\Delta^-$ Pearson $r$  $\Delta^-$ Spearman $\rho$
0.3700                  0.6870                      0.5099                 -0.6592                     -0.4676
0.6200                  0.7021                      0.5533                 -0.6817                     -0.5367
0.9100                  0.7028                      0.6138                 -0.6969                     -0.6159
0.9300                  0.7028                      0.6144                 -0.6963                     -0.6182

==================================================================
  tab:sensitivity-expert
==================================================================

   $s$  Pairs  Correct  Accuracy    $p$
0.3700     77       67    0.8701 0.0000
0.6200     77       64    0.8312 0.0000
0.9100     77       62    0.8052 0.0000
0.9300     77       62    0.8052 0.0000

  Observed (true D_misc), s = 0.93...
  Warning: 3 pair(s) dropped — review_id not found in attuned data.
    review_id_1=14144  review_id_2=18846
    review_id_1=13330  review_id_2=678
    review_id_1=18844  review_id_2=7083
  Note: 4 pair(s) marked unsure — counted as incorrect.
    Expert accuracy      : 0.8052  (n = 77)
    Delta+ vs D_misc (r) : 0.7028
    Delta- vs D_misc (r) : -0.6963

  Running 100 permutations of D_misc...
    10/100
    20/100
    30/100
    40/100
    50/100
    60/100
    70/100
    80/100
    90/100
    100/100

==================================================================
  PERMUTATION CONTROL
==================================================================

  expert_accuracy
    observed        : 0.8052
    permuted mean   : 0.6415  (SD 0.0902)
    permuted range  : [0.3704, 0.8148]
    permutations reaching observed: 2/100   p = 0.0297

  pos_pearson
    observed        : 0.7028
    permuted mean   : 0.2442  (SD 0.0391)
    permuted range  : [0.1320, 0.3574]
    permutations reaching observed: 0/100   p = 0.0099

  neg_pearson
    observed        : -0.6963
    permuted mean   : -0.1655  (SD 0.0438)
    permuted range  : [-0.2542, -0.0638]
    permutations reaching observed: 0/100   p = 0.0099