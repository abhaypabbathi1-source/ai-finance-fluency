import pandas as pd
import sqlite3

# --- Load a manageable sample, same approach as Day 21 ---
df = pd.read_csv("loans.csv", low_memory=False)
cols = ["loan_amnt", "int_rate", "grade", "term", "annual_inc", "loan_status"]
core = df[cols].sample(n=5000, random_state=42)

# --- Create a SQLite database file and write the data into it as a table ---
conn = sqlite3.connect("loans.db")
core.to_sql("loans", conn, if_exists="replace", index=False)

print("Database created. Table 'loans' has", len(core), "rows.")
conn.close()

# --- New: run SQL queries against the database ---
conn = sqlite3.connect("loans.db")

# SELECT + WHERE: pull only defaulted loans
query1 = """ 
SELECT loan_amnt, int_rate, grade, annual_inc
FROM loans
WHERE loan_status = 'Charged Off'
"""
defaults = pd.read_sql(query1,conn)
print("Defaulted loans found:", len(defaults))
print(defaults.head())

# ORDER BY: highest interest rates first
query2 = """
SELECT loan_amnt, int_rate, grade
FROM loans
ORDER BY int_rate DESC
LIMIT 5
"""
highest_rates = pd.read_sql(query2, conn)
print("\nTop 5 highest interest rate loans:")
print(highest_rates)

conn.close()