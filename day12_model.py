import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("loans.csv")
cols = ["loan_amnt","int_rate", "grade", "term", "annual_inc", "loan_status"]
core = df[cols].sample(n=5000, random_state=42)   

resolved = core[core["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
resolved["is_default"]=(resolved["loan_status"]=="Charged Off").astype(int)

grade_order = ["A", "B", "C", "D", "E", "F", "G"]
resolved["grade_num"] = resolved["grade"].astype(pd.CategoricalDtype(categories=grade_order,ordered=True)).cat.codes

resolved["term_months"] = resolved["term"].str.replace("months","",regex=False).astype(int)

features = resolved[["loan_amnt", "int_rate", "grade_num","annual_inc", "term_months"]]
target = resolved["is_default"]

X_train, X_test, y_train, y_test = train_test_split(
    features,target, test_size=0.2, random_state=42, stratify=target
)
print(X_train.shape, X_test.shape)
print(features.head())

print(resolved["is_default"].value_counts())

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

accuracy=model.score(X_test, y_test)
print("Test accuracy:", accuracy)

for name, coef in zip(features.columns,model.coef_[0]):
    print(name,":",coef)

baseline_accuracy = 1 - y_test.mean()
print("Baseline(never default) accuracy:", baseline_accuracy)