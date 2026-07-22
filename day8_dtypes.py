import pandas as pd

df = pd.read_csv("loans.csv", nrows=5000)
core = df[["loan_amnt", "int_rate", "grade", "loan_status", "annual_inc", "emp_length"]]
print(core.dtypes)
date_like = [c for c in df.columns if "date" in c.lower() or c.lower().endswith("_d")]
print(date_like)

core=df[["loan_amnt", "int_rate", "grade", "loan_status", "annual_inc", "emp_length", "issue_d"]]
print(core["issue_d"].head())
print(core["issue_d"].dtype)

core["issue_d"] = pd.to_datetime(core["issue_d"])
print(core["issue_d"].head())
print(core["issue_d"].dtype)

core["grade"] = core["grade"].astype("category")
print(core["grade"].dtype)
print(core["grade"].cat.categories)

grade_order = ["A", "B", "C", "D", "E", "F", "G"]
core["grade"] = core["grade"].astype(pd.CategoricalDtype(categories=grade_order, ordered=True))
print(core["grade"].dtype)
print(core.sort_values("grade")["grade"].head(10)) 
