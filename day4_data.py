import pandas as pd

df = pd.read_csv("loans.csv", nrows=5000)
print(df.head())

print(df.shape)
print(df.columns.tolist())
print(df[["loan_amnt", "int_rate", "grade", "loan_status"]].head())
