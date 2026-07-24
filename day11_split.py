import pandas as pd

df= pd.read_csv("loans.csv")
cols = ["loan_amnt","int_rate", "grade", "term","annual_inc","loan_status","total_rec_prncp", "recoveries", "last_pymnt_amnt","out_prncp"]
core = df[cols].sample(n=5000, random_state=42)
print(core.head())

resolved = core[core["loan_status"].isin(["Fully Paid","Charged Off"])].copy()
resolved["is_default"] = (resolved["loan_status"]=="Charged Off").astype(int)

print(resolved.groupby("is_default")[["total_rec_prncp","recoveries","last_pymnt_amnt", "out_prncp"]].mean())
print(resolved["is_default"].value_counts())

from sklearn.model_selection import train_test_split

features = resolved[["loan_amnt","int_rate", "grade", "term", "annual_inc"]].copy()
features["term_months"] = features["term"].str.replace("months","",regex=False).astype(int)
features = features.drop(columns=["term"])
target = resolved["is_default"]

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target

)

print("Train:",X_train.shape, "Test:", X_test.shape)
print("Train default rate:", y_train.mean())
print("Test default rate:", y_test.mean())