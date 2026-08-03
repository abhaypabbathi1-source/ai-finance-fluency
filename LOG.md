# Log
## Day 1
- Set up Python, VS Code, GitHub repo.
- Troubleshot Python Launcher confusion — turned out Terminal + python3 were working fine all along.
## Day 2
- Learned variables, lists, dicts, for loops, if/else statements
- Mapped each to Excel equivalents (list=column, dict=row, for=drag down, if= IF()).
- Big lesson: VS Code's Run button was using an old Python interpretor (no f-string support), not my actual code, causing a long confusing syntax error chase.
Fix: always run via python3 filename.py typed directly into Terminal.
## Day 3
- Learned functions: def, parameters, default values, return
- Combined if/for logic from Day 2 into functions that categorize and summarize loans
- Debugged: wrong python interpreter (no f-string support), a misspelled function name (loan_catagory vs loan_category) traced to its actual definition, and an IndentationError requiring a full rebuild of one code block.
-Lesson: always run with 'python3 filename.py' typed directly, and rebuild from scratch when indentation gets tangled rather than hunting spaces by eye

Separate task:
## Day 3
-Learned functions: def, parameters, default values, return.
Combined if/for logic into functions that categorize and summarize loans.
-Heavy debugging today: wrong interpreter, misspelled function name (loan_catagory), Indentation Error requiring a rebuild.
-Deliberately practiced reading 3 error types: TypeError (missing argument), NameError (misspelled name, with Python's auto-suggestion), and a silent None result from a missing return statement
## Day 4: loaded real data with Pandas
-Installed pandas, downloaded real Lending Club Data from Kaggle
- LOADED A 5,000 ROW SAMPLE WITH NROWS= to keep things fast.
- Learned .head(), .shape, .columns to explore a 145-column dataset.
-Filtered down to the columns that actually matter
- Set up .gitignore so the large raw CSV never gets committed to GitHub
## Day 5
-Learned git status, git log and git checkout
Created a practice branch, deliberately deleted LOG.md contents and committed that mistake on the practice branch only
Switched back to the main and confirmed it was completely untouched
Deleted practice branch with git branch -D
Big takeaway: branches let you make real,even committed mistakes in total safety.
## Day 6
- Learned filtering (boolean indexing with df[condition]), combining conditions
  with & for "and" logic, sorting with .sort_values(), and grouping with .groupby().
- Filtered loans over $20,000, then narrowed further to large loans with grade D.
- Sorted the dataset by interest rate to find the highest-rate loans.
- Used groupby to calculate average interest rate per credit grade — confirmed
  riskier grades (D) carry higher average rates than safer grades (A/B/C), matching
  real-world credit pricing intuition.
- Debugged a KeyError from a typo'd column name (loan_satus vs loan_status) —
  same typo pattern as Day 3's loan_catagory bug, now recognized instantly.
  ## Day 7
  Decision: dropping the emp_length column entirely rather than rows or filling, since employment length isn't relevant to this analysis and dropping the column preserves all 5,000 rows instead of losing 385 to missing data.
  - Learned .isnull(), .sum(), .dropna(), .fillna() for handling missing data.
- Checked missing % per column; found 7.7% missing in emp_length (only column with gaps).
- Hit a real error: .fillna(median()) fails on emp_length because it's text, not numeric — learned to check dtype before choosing a fill strategy.
- Decided to drop the emp_length column entirely (not just rows) because employment length isn't critical to this analysis, and dropping the column preserves all 5,000 rows instead of losing 385 to missing data.
- Noted 7.7% is higher than the current 4.2% unemployment rate, but resisted assuming unemployment as the cause without verifying it in the data — flagged as an open question rather than a conclusion.
## Day 8
- Learned about pandas dtypes: object/str, int64, float64, datetime64, category.
- Checked core.dtypes; confirmed loan_amnt/int_rate/annual_inc were already numeric, grade/loan_status/emp_length were str.
- Searched df.columns for date-like fields; found issue_d (populated for all rows) vs. hardship/settlement dates (only for a small subset).
- Converted issue_d from text ("Dec-2018") to real datetime64 using pd.to_datetime() — enables chronological sorting and date math.
- Converted grade to an ordered categorical (A < B < C < ... < G) instead of plain text — ensures correct sort order for future charts (Day 10) and a meaningful numeric encoding for the model (Day 11+).
- Key takeaway: correct dtypes aren't just cosmetic — wrong dtypes cause operations to silently do the wrong thing (e.g., alphabetical vs. risk-order sorting) rather than fail outright.
## Day 9
- Learned that numbers get stored as text when bundled with symbols/units (e.g. "36 months"), and that text categories can hide inconsistencies (case, whitespace, semantic duplicates).
- Cleaned term: stripped " months" text and cast to int (term_months) — now usable for filtering/math.
- Checked home_ownership: found 4 categories (RENT, MORTGAGE, OWN, ANY), no case inconsistencies. Decided to drop the 10 ANY rows — too rare (0.2%) to be meaningful.
- Checked emp_title: 2,927 unique values out of ~4,700 non-null rows — mostly free text, not a clean category set. Normalizing case/whitespace only reduced it to 2,471 (e.g. RN vs Registered Nurse still unmerged).
- Decided to bucket emp_title into rough industries via keyword matching instead of dropping — imperfect, "Other" absorbs most rows, but preserves some signal.
- Key takeaway: not every messy column deserves the same cleaning effort — knowing when a fix is "good enough" vs. not worth pursuing further is part of the skill.
- Hit a recurring VS Code autocomplete bug duplicating quotes when editing string literals near existing quotes — worked around by rewriting lines with single quotes.
## Day 10
- Learned matplotlib/seaborn basics for charting; used plt.savefig() to export PNGs for the portfolio.
- Discovered a sampling bias: the first 5000 rows of loans.csv were all recent (2018) loans, so none had resolved to Charged Off yet. Fixed by reading the full file and using .sample(5000, random_state=42) for a representative mix.
- Defined the target variable: is_default (1 = Charged Off, 0 = Fully Paid), restricted to resolved loans only (excluded Current/Late/In Grace Period since they haven't finished their term).
- Chart 1: default rate by grade — clean monotonic rise from ~7% (A) to ~64% (G), matching the ordered categorical set up on Day 8.
- Chart 2: default rate by income band — declining trend from ~23% (<$40K) to ~14% ($100K+), noisier than grade.
- Chart 3: default rate by term — 36 months ~16% vs 60 months ~29%, nearly double.
- Hit a real bug: matplotlib carried state across plots (forgot to clear the figure), causing two charts to overlay. Fixed with plt.figure()/plt.close() around each plot.
- Open question flagged for later (Day 15): are grade, income, and term independent signals, or partly confounded (e.g. lower grades disproportionately being 60-month loans)?
## Day 11
- Learned train/test split: evaluating a model on data it trained on gives artificially optimistic results.
- Learned leakage: features only known after a loan resolves (total_rec_prncp, recoveries, last_pymnt_amnt, out_prncp) would let the model "cheat" by reading the outcome instead of predicting it.
- Confirmed leakage empirically: total_rec_prncp averaged $14,348 for paid-off loans vs. $4,552 for defaults — a dead giveaway.
- Fixed a silent bug: "Fullyl Paid" typo in isin() caused every Fully Paid row to be dropped without an error — reinforced that string-matching typos fail quietly, not loudly.
- Built the actual split using sklearn's train_test_split with stratify=target: 2,323 train / 581 test rows, default rates nearly identical (19.24% vs 19.28%), confirming stratification worked.
- Features used: loan_amnt, int_rate, grade, annual_inc, term_months — all known at loan issuance, none leaked from the outcome.
## Day 12
- Learned logistic regression: predicts probability via a weighted sum of features passed through a sigmoid. Positive coefficients push toward default, negative push away.
- Encoded grade as grade_num using the ordered categorical from Day 8 (A=0 ... G=6), since sklearn needs numeric input.
- Hit two case-sensitivity bugs: "Charged off" vs "Charged Off" caused the same silent-filter-failure as Day 11's "Fullyl Paid" typo — reinforced that these bugs never crash, they just quietly produce wrong data.
- Trained LogisticRegression on loan_amnt, int_rate, grade_num, annual_inc, term_months. Coefficients matched intuition: int_rate (+) and grade_num (+) push toward default, annual_inc (-) pushes away, term_months (+) slightly.
- Test accuracy: 80.7%. Sanity-checked against a dumb "always predict no default" baseline: also 80.7% — identical. The model added zero measurable value on accuracy alone, almost certainly due to class imbalance (~19% default rate lets a lazy model hide behind a high accuracy number).
- Key humbling takeaway: accuracy is a misleading metric here. Flagged for Day 13/14 to properly diagnose whether the model actually learned anything real.
## Day 13
- Learned why accuracy is misleading on imbalanced data: a model can score high just by favoring the majority class.
- Fixed two typos: regax→regex in .str.replace(), and a stray period instead of comma in the train_test_split unpacking line.
- Computed confusion matrix, precision, recall, and AUC on the Day 12 model.
- Confusion matrix [[467,2],[110,2]]: model correctly identified 467/469 non-defaults, but only caught 2/112 actual defaults.
- Recall: 1.8% — model is nearly blind to defaults despite 80.7% accuracy. Precision: 0.5, but on only 4 total "predicted default" calls, not meaningful yet.
- AUC: 0.73 — meaningfully better than random (0.5), showing the model's predicted probabilities do rank risk correctly even though its default 0.5 threshold rarely gets crossed given the ~19% base rate.
- Key takeaway: the model wasn't useless, it was miscalibrated — accuracy hid a real signal (confirmed by AUC) while also hiding a real failure (confirmed by recall). Threshold tuning is a likely next fix, flagged for later.
## Day 14
- Compared model AUC (0.729) against a mathematically-defined baseline AUC (0.5) — the honest comparison, since accuracy alone ties the baseline.
- Tuned classification threshold instead of accepting the default 0.5 cutoff. Found threshold=0.4 beats baseline on every metric (accuracy 81.4%, precision 58.3%, recall 12.5%).
- Tested lower thresholds down to 0.15: recall jumps to 77.7% but accuracy drops to 58.2% and precision to 28.5% — a real cost/recall trade-off, not a free win like 0.4 was.
- Judgment call: picked 0.4 initially for balanced improvement, then reconsidered given asymmetric costs in lending (a missed default likely costs more than a false alarm) — concluded the "right" threshold depends on business costs not stated in the data itself.
- Proposed a two-stage design: use a high-recall threshold to flag broadly, then a secondary metric/model to differentiate true risk from false positives within the flagged set — sets up Day 15 (feature importance) as the natural next step to build that differentiator.
## Day 15
- Learned that raw logistic regression coefficients aren't comparable across features on different scales — standardized features with StandardScaler (fit on train only, to avoid leakage) before ranking importance.
- Scaled importance ranking: int_rate (0.292) and grade_num (0.286) nearly tied for most important, annual_inc (-0.105) a clear third, loan_amnt (0.083) and term_months (0.040) trailing. This differed meaningfully from the misleading raw-coefficient ranking in Day 12.
- Investigated the int_rate/grade_num near-tie, tying back to Day 10's open question about confounded features: found 0.95 correlation between them — LendingClub sets interest rate largely based on the grade it assigns, so the two features encode almost the same risk signal twice (multicollinearity).
- Decision: dropped grade_num, kept int_rate (continuous, more granular) as the primary risk signal.
- Verified empirically: AUC only dropped from 0.7288 to 0.7262 (negligible) after removing grade_num, and int_rate's coefficient grew to absorb the removed signal (0.292 -> 0.557) — confirming the two features were largely redundant, not two independent risk signals.
- Key takeaway: feature importance rankings can be unstable/misleading under multicollinearity; testing a simplification empirically (not just flagging the issue) is what makes the finding defensible.
## Day 16
- Refactored Days 6-15 into a single reproducible notebook (credit_risk_poc.ipynb) — the Month 1 deliverable.
- Structured into clear sections: intro, data cleaning/target definition, features/split, model training, evaluation, threshold tuning, and a plain-English summary of strengths/limitations.
- Reused the Day 15 simplified 4-feature model (dropped grade due to multicollinearity with int_rate).
- Verified numbers are consistent with prior days: 2,904 resolved loans, AUC 0.726, threshold 0.4 as the chosen operating point (81.6% accuracy, 60.9% precision, 12.5% recall).
- Wrote an honest limitations section: low recall even after tuning, small sample size, random (not chronological) train/test split, only 4 features, single model type tested so far.
## Day 17
- Learned random forest as an ensemble, non-linear alternative to logistic regression.
- Trained RandomForestClassifier (max_depth=5 to limit overfitting) on the same train/test split as the logistic regression model.
- Hit a bug: forgot to call roc_auc_score() with arguments, printed the function object itself instead of a number. Fixed by adding the (y_test, rf_proba) arguments.
- Honest comparison: Random Forest AUC 0.716 vs. Logistic Regression AUC 0.726 — logistic regression slightly won. A more complex model isn't automatically better, especially with only 4 features and a modest dataset.
- Cross-checked feature importance between both models: both independently rank int_rate > annual_inc > loan_amnt > term_months, strengthening confidence the ranking is real, not a modeling artifact.
- Final decision: kept logistic regression as the deliverable model — comparable performance, but interpretable coefficients matter in lending given fair lending regulations (ECOA) that require explainable credit decisions. A random forest's black-box nature is a real cost, not just an inconvenience, in this domain.
## Day 18
- Rewrote README.md as the project's front door: problem statement, data description, method summary, results, and an honest limitations section.
- Pulled together the full pipeline narrative (cleaning → target definition → leakage avoidance → feature selection → modeling → evaluation) into a readable summary for someone who hasn't seen the day-by-day process.
- Linked LOG.md from the README for anyone who wants the detailed build history.
## Day 19
- Ran an adversarial review of the whole project, ranking issues by severity: missing FICO/credit score, no cross-validation, random (not chronological) split, grade-vs-int_rate decision not tested both ways.
- Attempted to add fico_range_low as a feature — discovered this dataset doesn't include any FICO-related columns at all. Reclassified this from "oversight to fix" to "genuine data limitation."
- Added dti (debt-to-income ratio) instead — modest AUC improvement (0.726 -> 0.727), coefficient direction correct (higher dti -> higher default risk).
- Ran 5-fold cross-validation on the updated model. Key finding: cross-validated AUC (mean 0.686, std 0.038, range 0.63-0.74) is meaningfully lower than the single-split AUC (0.727) — the original number was optimistic due to relying on one train/test split.
- Updated the notebook's summary and limitations sections to report the honest cross-validated performance rather than the more flattering single-split number.
- Key takeaway: adversarial review isn't just about fixing bugs, it's about testing whether your own reported numbers hold up under scrutiny — they didn't fully, and documenting that is more credible than not checking.
## Day 21
- Learned k-fold cross-validation and why a single train/test split is unreliable.
- Ran 5-fold CV on logistic regression: mean AUC = 0.687, std = 0.0385.
- Fold scores ranged 0.631–0.739, showing meaningful split-to-split variance on 5000 rows.
## Day 22
- Ran GridSearchCV over C values [0.001, 0.01, 0.1, 1, 10, 100] with 5-fold CV.
- Best C = 0.1, AUC = 0.6868 — vs default C=1 AUC = 0.6866. Essentially no difference.
- All 6 C values scored within 0.0012 of each other, far inside yesterday's ~0.038 fold-to-fold noise.
- Conclusion: regularization strength isn't the bottleneck for this model. Ceiling is likely the linear model itself or the feature set — worth testing with gradient boosting (Day 23).
## Day 23
- Trained GradientBoostingClassifier (default settings) with 5-fold CV.
- Mean AUC = 0.666, std = 0.035 — worse than tuned logistic regression (0.687).
- Boosting likely overfitting on 5000 rows with default complexity (100 trees, depth 3).
- Updated hypothesis: ceiling may be the feature set, not model type — boosting didn't unlock better performance. Caveat: comparison isn't fully fair since boosting wasn't tuned like logistic regression was.
## Day 23 (continued)
- Tuned GradientBoostingClassifier with GridSearchCV over n_estimators/max_depth/learning_rate (27 combos, 5-fold CV).
- Best: learning_rate=0.01, max_depth=3, n_estimators=200 → AUC = 0.6834.
- Still below logistic regression's 0.6868, but gap (0.0034) is within noise (~0.035-0.038 std).
- Conclusion: model complexity is not the bottleneck — tuned boosting can't beat tuned logistic regression here. Ceiling is the feature set. Confirms direction for Week 6 (feature engineering).
## Day 24
- Plotted ROC curves for tuned logistic regression and tuned gradient boosting on the test split.
- Curves nearly overlap across all thresholds — visual confirmation both models extract similar signal from the same features.
- Single-split AUCs (0.729 log reg / 0.724 boosting) higher than CV means (0.687/0.683) — reinforces Day 21 lesson that single splits overstate performance.
- Saved plot as roc_curves.png.