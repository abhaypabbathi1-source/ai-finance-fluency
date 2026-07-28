import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

df=pd.read_csv("loans.csv")
cols = ["loan_amnt","int_rate", "grade", "term", "annual_inc","loan_status"]
core=df[cols].sample(n=5000, random_state=42)

resolved=core[core["loan_status"].isin(["Fully Paid","Charged Off"])].copy()
resolved["is_default"] = (resolved["loan_status"]=="Charged Off").astype(int)

grade_order = ["A","B","C","D","E","F","G"]
resolved["grade_num"]=resolved["grade"].astype(pd.CategoricalDtype(categories=grade_order,ordered=True)).cat.codes
resolved["term_months"]=resolved["term"].str.replace("months","",regex=False).astype(int)

features=resolved[["loan_amnt","int_rate","grade_num","annual_inc","term_months"]]
target=resolved["is_default"]

X_train,X_test,y_train,y_test = train_test_split(
    features,target,test_size=0.2, random_state=42, stratify=target

)

scaler=StandardScaler()
X_train_scaled=scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled,y_train)

for name,coef in sorted(zip(features.columns,model.coef_[0]),key=lambda x:abs(x[1]),reverse=True):
    print(name,":",coef)

    print(resolved[["int_rate","grade_num"]].corr())



features_v2 = resolved[["loan_amnt","int_rate","annual_inc","term_months"]]

X_train2,X_test2, y_train2, y_test2 = train_test_split(
        features_v2, target, test_size=0.2, random_state=42, stratify=target

    )
scaler2=StandardScaler()
X_train2_scaled=scaler2.fit_transform(X_train2)
X_test2_scaled = scaler2.transform(X_test2)

model2=LogisticRegression(max_iter=1000)
model2.fit(X_train2_scaled,y_train2)

from sklearn.metrics import roc_auc_score
y_proba2 = model2.predict_proba(X_test2_scaled)[:,1]
print("AUC without grade_num:", roc_auc_score(y_test2, y_proba2))
print("AUC with both(Day 14 baseline):",0.7288398568382577)

for name, coef in sorted(zip(features_v2.columns, model2.coef_[0]),key=lambda x: abs(x[1]),reverse=True):
    print(name,":",coef)
