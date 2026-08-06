import pandas as pd

df = pd.read_csv("loans.csv", low_memory=False)
cols = ["loan_amnt", "int_rate", "grade", "term", "annual_inc", "loan_status"]
core = df[cols].sample(n=5000, random_state=42)

resolved = core[core["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
resolved["is_default"] = (resolved["loan_status"] == "Charged Off").astype(int)

print(resolved["is_default"].value_counts())
print("\nDefault rate:", resolved["is_default"].mean())

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# --- Same feature prep as before ---
grade_order = ["A", "B", "C", "D", "E", "F", "G"]
resolved["grade_num"] = resolved["grade"].astype(
    pd.CategoricalDtype(categories=grade_order, ordered=True)
).cat.codes

resolved["term_months"] = resolved["term"].str.replace("months", "", regex=False).astype(int)

features = resolved[["loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months"]]
target = resolved["is_default"]

# --- New for Day 28: compare default vs. class_weight="balanced" ---
model_default = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=1000))
model_balanced = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=1000, class_weight="balanced"))

scores_default = cross_val_score(model_default, features, target, cv=5, scoring="roc_auc")
scores_balanced = cross_val_score(model_balanced, features, target, cv=5, scoring="roc_auc")

print("Default weighting — Mean AUC:", scores_default.mean(), "Std:", scores_default.std())
print("Balanced weighting — Mean AUC:", scores_balanced.mean(), "Std:", scores_balanced.std())

# --- New: check if the ~0.687 ceiling holds across a different random sample ---
core2 = df[cols].sample(n=5000, random_state=7)

resolved2 = core2[core2["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
resolved2["is_default"] = (resolved2["loan_status"] == "Charged Off").astype(int)

resolved2["grade_num"] = resolved2["grade"].astype(
    pd.CategoricalDtype(categories=grade_order, ordered=True)
).cat.codes

resolved2["term_months"] = resolved2["term"].str.replace("months", "", regex=False).astype(int)

features2 = resolved2[["loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months"]]
target2 = resolved2["is_default"]

scores_resample = cross_val_score(model_default, features2, target2, cv=5, scoring="roc_auc")

print("\nDifferent random sample (random_state=7) — Mean AUC:", scores_resample.mean(), "Std:", scores_resample.std())
print("Default rate in new sample:", target2.mean())