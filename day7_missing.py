import pandas as pd
df = pd.read_csv("loans.csv", nrows=5000)
core = df[["loan_amnt", "int_rate", "grade", "loan_status", "annual_inc", "emp_length"]]

print(core.isnull().sum())

missing_pct = (core.isnull().sum() / len(core)) * 100
print(missing_pct)

missing_emp = core[core["emp_length"].isnull()]
print(missing_emp.head())

dropped = core.dropna()
print(len(core), "->", len(dropped))

filled = core.copy()
filled["annual_inc"] = filled["annual_inc"].fillna(filled["annual_inc"].median())
print(filled["annual_inc"].isnull().sum())

filled = core.copy()
filled["emp_length"] = filled["emp_length"].fillna("Unknown")
print(filled["emp_length"].isnull().sum())

core_no_emp = core.drop(columns=["emp_length"])
print(core_no_emp.columns)
print(len(core_no_emp))