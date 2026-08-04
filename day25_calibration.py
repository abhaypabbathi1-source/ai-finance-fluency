import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.calibration import calibration_curve

# --- Same data prep as Days 21-24 ---
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

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target
)

# --- Train both tuned models, same as Day 24 ---
logreg = LogisticRegression(C=0.1, max_iter=1000)
logreg.fit(X_train, y_train)

boosting = GradientBoostingClassifier(
    n_estimators=200, max_depth=3, learning_rate=0.01, random_state=42
)
boosting.fit(X_train, y_train)

logreg_probs = logreg.predict_proba(X_test)[:, 1]
boosting_probs = boosting.predict_proba(X_test)[:, 1]

# --- New for Day 25: calibration curves ---
frac_pos_log, mean_pred_log = calibration_curve(y_test, logreg_probs, n_bins=10)
frac_pos_gb, mean_pred_gb = calibration_curve(y_test, boosting_probs, n_bins=10)

plt.plot(mean_pred_log, frac_pos_log, marker="o", label="Logistic Regression")
plt.plot(mean_pred_gb, frac_pos_gb, marker="o", label="Gradient Boosting")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfectly calibrated")

plt.xlabel("Mean Predicted Probability")
plt.ylabel("Actual Fraction of Defaults")
plt.title("Calibration Curve: Logistic Regression vs Gradient Boosting")
plt.legend()
plt.savefig("calibration_curves.png")
plt.show()