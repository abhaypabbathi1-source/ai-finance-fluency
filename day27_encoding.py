import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

df=pd.read_csv("loans.csv", low_memory=False)

print("emp_length values:")
print(df["emp_length"].value_counts(dropna=False))

print("\nhome_ownership values:")
print(df["home_ownership"].value_counts(dropna=False))

#--- Same data prep as Days 21-26 ---

cols = ["loan_amnt", "int_rate", "grade", "term", "annual_inc", "loan_status",
        "emp_length", "home_ownership"]
core = df[cols].sample(n=5000, random_state=42)

resolved = core[core["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
resolved["is_default"] = (resolved["loan_status"] == "Charged Off").astype(int)

grade_order = ["A", "B", "C", "D", "E", "F", "G"]
resolved["grade_num"] = resolved["grade"].astype(
    pd.CategoricalDtype(categories=grade_order, ordered=True)
).cat.codes

resolved["term_months"] = resolved["term"].str.replace("months", "", regex=False).astype(int)

#--- New for Day 27: encode emp_length as an ordered scale ---
emp_order = ["< 1 year", "1 year","2 years","3 years","4 years", "5 years","6 years", "7 years", "8 years", "9 years", "10+ years"]

resolved["emp_length"] = resolved["emp_length"].fillna("Missing")
emp_categories = emp_order + ["Missing"]

resolved["emp_length_num"] = resolved["emp_length"].astype(
    pd.CategoricalDtype(categories=emp_categories, ordered=True)

).cat.codes

# --- New for Day 27: collapse rate home_ownership categories, then one-hot encode ---
resolved["home_ownership"] = resolved["home_ownership"].replace(
    {"ANY": "OTHER", "NONE": "OTHER"}

)
home_dummies = pd.get_dummies(resolved["home_ownership"], prefix="home", drop_first=True)
resolved = pd.concat([resolved, home_dummies], axis=1)

print(resolved[["emp_length", "emp_length_num", "home_ownership"]].head(10))
print("\nNew home owenership columns:", list(home_dummies.columns))

#--- New for DAY 27: TEST NEW FEATURES AGAinst baseline ---

# --- New for Day 27: test new features against baseline ---
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

target = resolved["is_default"]
model = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=1000))

original_features = resolved[["loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months"]]

new_features = resolved[[
    "loan_amnt", "int_rate", "grade_num", "annual_inc", "term_months",
    "emp_length_num"
] + list(home_dummies.columns)]

scores_original = cross_val_score(model, original_features, target, cv=5, scoring="roc_auc")
scores_new = cross_val_score(model, new_features, target, cv=5, scoring="roc_auc")

print("Original features — Mean AUC:", scores_original.mean(), "Std:", scores_original.std())
print("With emp_length + home_ownership — Mean AUC:", scores_new.mean(), "Std:", scores_new.std())