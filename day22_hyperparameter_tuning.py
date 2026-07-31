import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

# --- Same data prep as Day 21 ---
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

# --- New for Day 22: search over C values ---

model = LogisticRegression(max_iter=1000)

param_grid={"C":[0.001,0.01,0.1,1,10,100]}

grid = GridSearchCV(model,param_grid, cv=5, scoring="roc_auc")
grid.fit(features,target)

print("Best C:", grid.best_params_)
print("Best mean AUC:",grid.best_score_)

# See every value tested, not just the winner

results=pd.DataFrame(grid.cv_results_)
print(results[["param_C","mean_test_score","std_test_score"]])
