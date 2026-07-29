import pandas as pd
df = pd.read_csv("loans.csv", nrows=5000)
messy = df[["term", "revol_util", "emp_title", "home_ownership"]]
print(messy.head(10))
print(messy.dtypes)

messy["term_months"] = messy["term"].str.replace(" months", "", regex=False).astype(int)
print(messy[["term", "term_months"]].head())
print(messy["term_months"].dtype)

print(messy["home_ownership"].unique())
print(messy["home_ownership"].value_counts())

print(messy["emp_title"].nunique())
print(messy["emp_title"].value_counts().head(10))

messy["emp_title_clean"] = messy["emp_title"].str.strip().str.lower()
print(messy["emp_title_clean"].nunique())

# Decision: normalizing case/whitespace fixes exact-duplicate issues (Teacher vs teacher),
# but doesn't merge semantic duplicates (RN vs Registered Nurse) — that would need
# more advanced text matching. Given emp_title isn't critical to this analysis,
# dropping it is more practical than investing in full text cleaning here.


# Decision: dropping the 10 "ANY" rows in home_ownership — too rare (0.2% of data)
# to be a meaningful category, and dropping is cheap since it's only 10 rows.
home_clean = messy[messy["home_ownership"] != "ANY"]
print(len(messy), "->", len(home_clean))

# Decision: bucketing emp_title into rough industries via keyword matching,
# rather than dropping the column entirely — imperfect (catches obvious cases only,
# "Other" absorbs everything else), but preserves some signal instead of none.

def bucket_title(title):
    if pd.isna(title):
        return "Unknown"
    t = title.lower()
    if "teach" in t or "professor" in t:
        return "Education"
    elif "nurse" in t or "rn" in t or "health" in t or "medical" in t:
        return "Healthcare"
    elif "manager" in t or "director" in t or "supervisor" in t:
        return "Management"
    elif "sales" in t:
        return "Sales"
    else:
        return "Other"
    
messy["emp_title_bucket"] = messy["emp_title_clean"].apply(bucket_title)
print(messy["emp_title_bucket"].value_counts())
  