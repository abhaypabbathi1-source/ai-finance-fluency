import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

# --- Same data prep as Day 21/22 ---
df = pd.read_csv("loans.csv", low_memory=False)
cols = ["loan_amnt", "int_rate", "grade", "term", "annual_inc", "loan_status"]
core = df[cols].sample(n=5000, random_state=42)

resolved = core[core["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
resolved["is_default"] = (resolved["loan_status"] == "Charged Off").astype(int)

grade_order = ["A", "B", "C", "D", "E", "F", "G"]
resolved["grade_num"] = resolved["grade"].astype(
    pd.CategoricalDtype(categories=grade_order, ordered=True)
).cat.codes

resolved["term_months"] = resolved["term"].str.replace("months", "", regex=False).astype(int)

features = resolved[["loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months"]]
target = resolved["is_default"]

#--- New for Day 23: Gradient boosting instead of Logsitic Regression

model = GradientBoostingClassifier (random_state=42)

scores = cross_val_score(model,features,target,cv=5, scoring ="roc_auc")

print("AUC per fold:",scores)
print("Mean AUC:", scores.mean())
print("Std dev:", scores.std())