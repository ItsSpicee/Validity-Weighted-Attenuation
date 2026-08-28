=== Stage 4: Regression ===
Building feature matrix...
  Loading clause vectors...
  Pivoting to per-review emotion features...
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\data\processed\final_emotions.csv
Running 5-fold cross-validation...
0:      learn: 1.1789905        total: 152ms    remaining: 2m 32s
100:    learn: 0.6489469        total: 879ms    remaining: 7.82s
200:    learn: 0.5967434        total: 1.59s    remaining: 6.34s
300:    learn: 0.5778310        total: 2.3s     remaining: 5.34s
400:    learn: 0.5650791        total: 3.11s    remaining: 4.65s
500:    learn: 0.5543732        total: 3.82s    remaining: 3.81s
600:    learn: 0.5436505        total: 4.52s    remaining: 3s
700:    learn: 0.5331758        total: 5.25s    remaining: 2.24s
800:    learn: 0.5241183        total: 6.02s    remaining: 1.5s
900:    learn: 0.5152983        total: 7.64s    remaining: 839ms
999:    learn: 0.5067870        total: 9.43s    remaining: 0us
  Fold 1: MAE=0.6396  Spearman=0.7461  R²=0.6212
0:      learn: 1.1873383        total: 19.1ms   remaining: 19.1s
100:    learn: 0.6507826        total: 1.8s     remaining: 16.1s
200:    learn: 0.5991111        total: 3.62s    remaining: 14.4s
300:    learn: 0.5805296        total: 5.4s     remaining: 12.5s
400:    learn: 0.5683515        total: 7.13s    remaining: 10.7s
500:    learn: 0.5576344        total: 8.81s    remaining: 8.78s
600:    learn: 0.5470510        total: 10.5s    remaining: 6.97s
700:    learn: 0.5358895        total: 12.2s    remaining: 5.2s
800:    learn: 0.5262024        total: 13.9s    remaining: 3.45s
900:    learn: 0.5172495        total: 15.6s    remaining: 1.71s
999:    learn: 0.5089847        total: 17.3s    remaining: 0us
  Fold 2: MAE=0.6254  Spearman=0.7206  R²=0.6197
0:      learn: 1.1725767        total: 18.6ms   remaining: 18.5s
100:    learn: 0.6487496        total: 1.73s    remaining: 15.4s
200:    learn: 0.5970161        total: 3.45s    remaining: 13.7s
300:    learn: 0.5782120        total: 5.15s    remaining: 12s
400:    learn: 0.5656263        total: 6.86s    remaining: 10.2s
500:    learn: 0.5550557        total: 8.58s    remaining: 8.54s
600:    learn: 0.5436455        total: 10.3s    remaining: 6.82s
700:    learn: 0.5332910        total: 11.9s    remaining: 5.1s
800:    learn: 0.5241460        total: 13.6s    remaining: 3.39s
900:    learn: 0.5153137        total: 15.3s    remaining: 1.68s
999:    learn: 0.5073050        total: 17s      remaining: 0us
  Fold 3: MAE=0.6373  Spearman=0.7433  R²=0.6385
0:      learn: 1.1880646        total: 18.8ms   remaining: 18.8s
100:    learn: 0.6520003        total: 1.73s    remaining: 15.4s
200:    learn: 0.5999652        total: 3.47s    remaining: 13.8s
300:    learn: 0.5815631        total: 5.17s    remaining: 12s
400:    learn: 0.5687895        total: 6.87s    remaining: 10.3s
500:    learn: 0.5587178        total: 8.55s    remaining: 8.52s
600:    learn: 0.5476780        total: 10.2s    remaining: 6.8s
700:    learn: 0.5369223        total: 11.9s    remaining: 5.09s
800:    learn: 0.5277648        total: 13.6s    remaining: 3.38s
900:    learn: 0.5186266        total: 15.3s    remaining: 1.68s
999:    learn: 0.5112355        total: 17s      remaining: 0us
  Fold 4: MAE=0.6306  Spearman=0.7046  R²=0.6151
0:      learn: 1.1881163        total: 18.5ms   remaining: 18.5s
100:    learn: 0.6538615        total: 1.73s    remaining: 15.4s
200:    learn: 0.6020815        total: 3.44s    remaining: 13.7s
300:    learn: 0.5835558        total: 5.15s    remaining: 12s
400:    learn: 0.5709485        total: 6.85s    remaining: 10.2s
500:    learn: 0.5609344        total: 8.54s    remaining: 8.5s
600:    learn: 0.5507259        total: 10.2s    remaining: 6.78s
700:    learn: 0.5415021        total: 11.9s    remaining: 5.08s
800:    learn: 0.5317005        total: 13.6s    remaining: 3.38s
900:    learn: 0.5230116        total: 15.3s    remaining: 1.68s
999:    learn: 0.5147456        total: 17s      remaining: 0us
  Fold 5: MAE=0.6172  Spearman=0.7273  R²=0.6329

  CV Mean MAE:      0.6300 ± 0.0081
  CV Mean Spearman: 0.7284 ± 0.0152
  CV Mean R²:       0.6255 ± 0.0088
Training final model...
0:      learn: 1.1828000        total: 19.6ms   remaining: 19.5s
100:    learn: 0.6540764        total: 1.78s    remaining: 15.9s
200:    learn: 0.6045360        total: 3.54s    remaining: 14.1s
300:    learn: 0.5880591        total: 5.28s    remaining: 12.3s
400:    learn: 0.5768066        total: 7.07s    remaining: 10.6s
500:    learn: 0.5676102        total: 8.8s     remaining: 8.76s
600:    learn: 0.5581535        total: 10.5s    remaining: 6.99s
700:    learn: 0.5489230        total: 12.3s    remaining: 5.22s
800:    learn: 0.5405561        total: 14s      remaining: 3.47s
900:    learn: 0.5322119        total: 15.7s    remaining: 1.72s
999:    learn: 0.5243609        total: 17.4s    remaining: 0us

  Final test (unseen professors):
  MAE=0.6347  Spearman=0.7352  Pseudo R²=0.6168
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\models\cat_boost_final.cbm
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\models\final_feature_importance.csv

=== Stage 5: Attenuation ===
Loading model and data...
  Using s = 1.0 (fixed a priori, not tuned)
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\data\processed\weighted_emotions.csv
  Held-out reviews (misc subset): 2,052 of 10,375

  Total ratings attuned:        60.58%
  Ratings increased:            31.96%
  Ratings decreased:            28.62%
  Max |Δ|:                      2.7103
  Mean |Δ| (adjusted reviews):  0.1964
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\data\processed\attuned_ratings.csv
  Saved: C:\Users\raiha\Desktop\Git\Validity-Weighted-Attenuation\data\processed\attuned_ratings_full.csv

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
  Pairs evaluated : 43  (3 unsure → incorrect)
  Correct         : 38
  Accuracy        : 88.4%
  Binomial p-value (vs. chance = 0.5): 0.0000001

  ────────────────────────────────────────────────
  Fine    (0 ≤ Difference in |Δ| < 0.5)
  ────────────────────────────────────────────────
  Pairs evaluated : 34  (1 unsure → incorrect)
  Correct         : 24
  Accuracy        : 70.6%
  Binomial p-value (vs. chance = 0.5): 0.0121533

  Bins partition the pairs: 77 of 77 assigned.
=== Stage 7: Robustness ===
Loading model and data...

  s values: [0.5, 0.75, 1.0, 1.25, 1.5]   (pipeline uses S_VALUE = 1.0)
  Held-out misc reviews: 2,052

==================================================================
  tab:sensitivity-delta-agreement
==================================================================

 $s_a$  $s_b$  Pearson $r$  Spearman $\rho$  Mean $|\Delta_a - \Delta_b|$  Max $|\Delta_a - \Delta_b|$
0.5000 0.7500       0.9914           0.9165                        0.0427                       0.4066
0.5000 1.0000       0.9803           0.8243                        0.0629                       0.8358
0.5000 1.2500       0.9712           0.7545                        0.0742                       1.0260
0.5000 1.5000       0.9635           0.6887                        0.0830                       1.1482
0.7500 1.0000       0.9953           0.9198                        0.0294                       0.4292
0.7500 1.2500       0.9899           0.8479                        0.0425                       0.6194
0.7500 1.5000       0.9845           0.7805                        0.0521                       0.7416
1.0000 1.2500       0.9973           0.9165                        0.0216                       0.2654
1.0000 1.5000       0.9941           0.8528                        0.0311                       0.3719
1.2500 1.5000       0.9982           0.9190                        0.0168                       0.1729

==================================================================
  tab:sensitivity-modulators
==================================================================
   $s$  $\Delta^+$ Pearson $r$  $\Delta^+$ Spearman $\rho$  $\Delta^-$ Pearson $r$  $\Delta^-$ Spearman $\rho$
0.5000                  0.6765                      0.5046                 -0.6880                     -0.5020
0.7500                  0.6837                      0.5756                 -0.7031                     -0.5421
1.0000                  0.6872                      0.6142                 -0.7077                     -0.6001
1.2500                  0.6858                      0.6557                 -0.7094                     -0.6464
1.5000                  0.6769                      0.6800                 -0.7167                     -0.6942

==================================================================
  tab:sensitivity-expert
==================================================================

   $s$  Pairs  Overall  Coarse   Fine    $p$
0.5000     77   0.8571  0.8750 0.8276 0.0000
0.7500     77   0.8571  0.8750 0.8276 0.0000
1.0000     77   0.8052  0.8837 0.7059 0.0000
1.2500     77   0.8442  0.8810 0.8000 0.0000
1.5000     77   0.8182  0.8718 0.7632 0.0000



  Running 1000 permutations of D_misc...
    10/1000
    ...
    1000/1000

==================================================================
  PERMUTATION CONTROL
==================================================================

  expert_accuracy
    observed        : 0.8052
    permuted mean   : 0.6061  (SD 0.0464)
    permuted range  : [0.4675, 0.7532]
    permutations reaching observed: 0/1000   p = 0.0010

  pos_pearson
    observed        : 0.6872
    permuted mean   : 0.2327  (SD 0.0291)
    permuted range  : [0.1278, 0.3235]
    permutations reaching observed: 0/1000   p = 0.0010

  neg_pearson
    observed        : -0.7077
    permuted mean   : -0.1579  (SD 0.0374)
    permuted range  : [-0.2744, -0.0476]
    permutations reaching observed: 0/1000   p = 0.0010

    ==================================================================
  BOOTSTRAP PROFESSOR STABILITY (held-out professors)
==================================================================

  Δ+ vs D_misc (Pearson r)
    mean: 0.6855   SD: 0.0184
    95% CI: [0.6494, 0.7210]

  Δ- vs D_misc (Pearson r)
    mean: -0.7079   SD: 0.0182
    95% CI: [-0.7434, -0.6736]

  Δ+ vs D_misc (Spearman ρ)
    mean: 0.6144   SD: 0.0272
    95% CI: [0.5647, 0.6619]

  Δ- vs D_misc (Spearman ρ)
    mean: -0.6014   SD: 0.0252
    95% CI: [-0.6468, -0.5581]
