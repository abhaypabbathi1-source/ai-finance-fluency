import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_score, recall_score, confusion_matrix

df = pd.read_csv("loans.csv")
cols = ["loan_amnt", "int_rate", "grade", "term", "annual_inc","loan_status"]
core = df[cols].sample(n=5000, random_state=42)

resolved=core[core["loan_status"].isin(["Fully Paid","Charged Off"])].copy()
resolved["is_default"]=(resolved["loan_status"]=="Charged Off").astype(int)

grade_order = ["A","B","C","D","E","F","G"]
resolved["grade_num"]=resolved["grade"].astype(pd.CategoricalDtype(categories=grade_order,ordered=True)).cat.codes
resolved["term_months"]=resolved["term"].str.replace("months","", regex=False).astype(int)

features=resolved[["loan_amnt","int_rate","grade_num","annual_inc","term_months"]]
target=resolved["is_default"]

X_train,X_test,y_train,y_test=train_test_split(
    features,target,test_size=0.2,random_state=42,stratify=target

)
model=LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_proba=model.predict_proba(X_test)[:,1]

print("Model AUC:", roc_auc_score(y_test,y_proba))
print("Baseline AUC:",0.5)

for threshold in [0.5,0.4,0.3,0.15]:
    y_pred_thresh = (y_proba >= threshold).astype(int)
    precision = precision_score(y_test, y_pred_thresh, zero_division=0)
    recall = recall_score(y_test,y_pred_thresh, zero_division=0)
    accuracy = (y_pred_thresh == y_test).mean()
    print(f"Threshold {threshold}: accuracy={accuracy:.3f}, precision={precision:.3f}, recall={recall:.3f}")