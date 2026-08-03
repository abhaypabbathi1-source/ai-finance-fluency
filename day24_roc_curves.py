import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

# --- Same data prep as Days 21-23 ---
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

# --- New for Day 24: a single train/test split, since we need actual predictions to plot ---
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target
)

#--- New for day 24: train final versions of both models ---

logreg=LogisticRegression(C=0.1, max_iter=1000)
logreg.fit(X_train, y_train)

boosting = GradientBoostingClassifier(
    n_estimators=200, max_depth=3, learning_rate=0.01, random_state=42
)
boosting.fit(X_train,y_train)

logreg_probs = logreg.predict_proba(X_test)[:,1]
boosting_probs = boosting.predict_proba(X_test)[:,1]

fpr_log,tpr_log, _ = roc_curve(y_test,logreg_probs)
fpr_gb, tpr_gb, _ = roc_curve(y_test,boosting_probs)

auc_log = roc_auc_score(y_test, logreg_probs)
auc_gb= roc_auc_score(y_test, boosting_probs)

plt.plot(fpr_log, tpr_log, label=f"Logistic Regression (AUC={auc_log:3f})")
plt.plot(fpr_gb, tpr_gb, label=f"Gradient Boosting (AUC={auc_gb:3f})")
plt.plot([0,1],[0,1], linestyle="--", color="gray", label="Random Guess")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Roc Curve: Logistic Regression vs Gradient Boosting")
plt.legend()
plt.savefig("roc_curves.png")
plt.show()