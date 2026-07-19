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