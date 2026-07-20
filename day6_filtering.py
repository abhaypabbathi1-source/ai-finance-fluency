import pandas as pd
df = pd.read_csv("loans.csv", nrows=5000)
core = df[["loan_amnt", "int_rate", "grade", "loan_status", "annual_inc"]]
print(core.head())

large_loans = core[core["loan_amnt"] > 20000]
print(large_loans.head())
print(len(large_loans))

big_risky_loans = core[(core["loan_amnt"] > 20000) & (core["grade"].isin(["D", "E", "F", "G"]))]
print(big_risky_loans.head())
print(len(big_risky_loans))

high_risk_or_rate = core[(core["grade"].isin(["D", "E", "F", "G"])) | (core["int_rate"] > 20)]
print(len(high_risk_or_rate))

not_current = core[~(core["loan_status"] == "Current")]
print(not_current["loan_status"].value_counts())
                  
