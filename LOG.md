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