import pandas as pd
df = pd.read_csv("loans.csv", nrows=5000)
core = df[["loan_amnt", "int_rate", "grade", "loan_status", "annual_inc", "term"]]
print(core["loan_status"].value_counts())

import pandas as pd
df = pd.read_csv("loans.csv")
core = df[["loan_amnt", "int_rate", "grade", "loan_status", "annual_inc", "term"]].sample(n=5000, random_state=42)
print(core["loan_status"].value_counts())

#Dont want to include charged off loans as they are not in the basket of resolved loans, need to get rid of them

resolved = core[core["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
resolved["is_default"] = (resolved["loan_status"] == "Charged Off").astype(int)
print(len(core), "->", len(resolved))
print(resolved["is_default"].value_counts())

import matplotlib.pyplot as plt

default_by_grade = resolved.groupby("grade")["is_default"].mean().sort_index()
print(default_by_grade)

default_by_grade.plot(kind="bar" , color="steelblue")
plt.title("Default Rate by Loan Grade")
plt.ylabel(" Default Rate")
plt.xlabel("Grade")
plt.tight_layout()
plt.savefig("default_by_grade.png")
print("Saved chart to default_by_grade.png")
plt.close()

resolved["income_band"] = pd.cut(
    resolved["annual_inc"],
    bins=[0,40000,60000,80000,100000, float("inf")],
    labels=["<40k", "40-60k", "60-80k", "80-100k", "100k+"]

)
default_by_income = resolved.groupby("income_band", observed=True)["is_default"].mean()
print(default_by_income)

default_by_income.plot(kind="bar", color="darkorange")
plt.title("Default Rate by Income Band")
plt.ylabel("Default Rate")
plt.xlabel("Income Band")
plt.tight_layout()
plt.savefig("default_by_income.png")
print("Saved chart to default_by_income.png")
plt.close()

default_by_term = resolved.groupby("term")["is_default"].mean()
print(default_by_term)

plt.figure()
default_by_term.plot(kind="bar", color="seagreen")
plt.title("Default Rate by Loan Term")
plt.ylabel("Default Rate")
plt.xlabel("Term")
plt.tight_layout()
plt.savefig("default_by_term.png")
plt.close()
print("Saved chart to default_by_term.png")
