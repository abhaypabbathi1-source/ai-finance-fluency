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