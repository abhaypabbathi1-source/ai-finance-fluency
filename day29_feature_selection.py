import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance

# --- Fast read: limit rows at load time, not after ---
df = pd.read_csv("loans.csv", low_memory=False, nrows=500000)

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

# --- New for Day 29: correlation between features ---
print("Feature correlation matrix:")
print(features.corr())

# --- New for Day 29: permutation importance ---
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target
)

model = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=1000))
model.fit(X_train, y_train)

result = permutation_importance(
    model, X_test, y_test, scoring="roc_auc", n_repeats=30, random_state=42
)

importance_df = pd.DataFrame({
    "feature": features.columns,
    "importance_mean": result.importances_mean,
    "importance_std": result.importances_std
}).sort_values("importance_mean", ascending=False)

print("\nPermutation importance (drop in AUC when shuffled):")
print(importance_df)

df = pd.read_csv("loans.csv", low_memory=False, nrows=50000)
core = df[cols].sample(n=5000, random_state=42)