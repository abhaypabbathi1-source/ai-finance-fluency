import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

# --- Load data ---
df = pd.read_csv("loans.csv", low_memory=False)

cols = ["int_rate", "grade", "annual_inc", "loan_status"]
core = df[cols].sample(n=5000, random_state=42)

resolved = core[core["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
resolved["is_default"] = (resolved["loan_status"] == "Charged Off").astype(int)

grade_order = ["A", "B", "C", "D", "E", "F", "G"]
resolved["grade_num"] = resolved["grade"].astype(
    pd.CategoricalDtype(categories=grade_order, ordered=True)
).cat.codes

# --- Final feature set, trimmed based on Day 29 permutation importance ---
features = resolved[["int_rate", "grade_num", "annual_inc"]]
target = resolved["is_default"]

# --- Model: scaling + tuned logistic regression, bundled as one pipeline ---
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(C=0.1, max_iter=1000)
)

# --- Evaluate with cross-validation, same rigor as Week 5 ---
scores = cross_val_score(model, features, target, cv=5, scoring="roc_auc")

print("Final model — Mean AUC:", scores.mean(), "Std:", scores.std())
print("(Compare to Day 21 5-feature baseline: 0.6866)")