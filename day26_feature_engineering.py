import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# --- Same data prep as Days 21-25 ---
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

#--- New for day 26: derived features ---

# Debt to income style ratio: how large is this loan relative to what they earn?
resolved["loan_to_income"] = resolved["loan_amnt"]/resolved["annual_inc"]

# Interest burden: combines rate and loan size into one number representing rough cost of borrowing
resolved["rate_x_amount"] = resolved["int_rate"] * resolved["loan_amnt"]

# Monthly payment burden relative to income (rough approximation, no compouding)
resolved["est_monthly_payment"] = resolved["loan_amnt"] /resolved["term_months"]
resolved["payment_to_income"] = resolved["est_monthly_payment"]/ (resolved["annual_inc"]/12)

# --- New for day 26: compare original features vs. original + engineered ---

target =resolved["is_default"]

original_features = resolved[["loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months"]]

engineered_features = resolved[[
    "loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months",
    "loan_to_income", "rate_x_amount", "payment_to_income"

]]

model = LogisticRegression(C=0.1,max_iter=1000)

scores_original = cross_val_score(model,original_features, target, cv=5, scoring="roc_auc")
scores_engineered = cross_val_score(model, engineered_features, target, cv=5, scoring="roc_auc")

print("Original features - Mean AUC:", scores_original.mean(), "Std:", scores_original.std())
print("Engineered features - Mean AUC:", scores_engineered.mean(), "Std:", scores_engineered.std())

# --- Testing each engineered feature individually ---

feature_sets = {
    "original + loan_to_income": ["loan_amnt","int_rate", "grade_num", "annual_inc", "term_months", "loan_to_income"],
    "original + rate_x_amount": ["loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months","rate_x_amount"],
    "original + payment_to_income": ["loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months", "payment_to_income"],

}

for name, cols in feature_sets.items():
    X = resolved[cols]
    scores = cross_val_score(model, X, target, cv=5, scoring="roc_auc")
    print(f"{name} - Mean AUC: {scores.mean(): .4f} Std:{scores.std(): .4f}")