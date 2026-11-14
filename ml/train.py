
import pandas as pd
import numpy as np
import joblib
import time

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

start_time = time.time()

# 1. Load dataset
print("Loading dataset...")

df = pd.read_csv("data\indian_banking_transactions.csv")

print("Original Dataset Shape:", df.shape)

# 2. Handle missing loan type
df.loc[
    (df["has_loan"] == 0) & (df["loan_type"].isna()),
    "loan_type"
] = "No Loan"

df.loc[
    (df["has_loan"] == 1) & (df["loan_type"].isna()),
    "loan_type"
] = "Unknown"

# 3. Extract date features
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"], errors="coerce"
)

df["year"] = df["transaction_date"].dt.year
df["month"] = df["transaction_date"].dt.month
df["day"] = df["transaction_date"].dt.day
df["day_of_week"] = df["transaction_date"].dt.dayofweek
df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)

# 4. Drop unnecessary columns
df.drop(
    columns=[
        "transaction_id",
        "customer_id",
        "transaction_time",
        "transaction_date"
    ],
    inplace=True
)

# 5. Separate features and target
X = df.drop("is_fraud", axis=1)
y = df["is_fraud"]

# 6. Identify categorical and numerical columns
categorical_cols = X.select_dtypes(
    include=["object", "category", "str"]
).columns.tolist()

numerical_cols = X.select_dtypes(
    include=["number", "bool"]
).columns.tolist()

print("\nCategorical Columns:", categorical_cols)
print("Numerical Columns:", numerical_cols)

# 7. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)

# 8. Encode categorical columns
encoder = OneHotEncoder(
    drop="first",
    handle_unknown="ignore",
    sparse_output=False
)

X_train_encoded = encoder.fit_transform(
    X_train[categorical_cols]
)

X_test_encoded = encoder.transform(
    X_test[categorical_cols]
)

encoded_cols = encoder.get_feature_names_out(
    categorical_cols
)

# 9. Combine numerical and encoded columns
X_train_final = pd.concat(
    [
        X_train[numerical_cols].reset_index(drop=True),
        pd.DataFrame(
            X_train_encoded,
            columns=encoded_cols
        )
    ],
    axis=1
)

X_test_final = pd.concat(
    [
        X_test[numerical_cols].reset_index(drop=True),
        pd.DataFrame(
            X_test_encoded,
            columns=encoded_cols
        )
    ],
    axis=1
)

print("\nFinal Training Shape:", X_train_final.shape)
print("Final Testing Shape:", X_test_final.shape)

# 10. Train Gradient Boosting model
print("\nTraining Gradient Boosting Model...")

model = GradientBoostingClassifier(
    n_estimators=50,
    learning_rate=0.1,
    max_depth=2,
    min_samples_leaf=10,
    random_state=42
)

model.fit(X_train_final, y_train)

print("Model training completed!")

# 11. Predictions
threshold = 0.05

y_probability = model.predict_proba(X_test_final)[:, 1]
y_pred = (y_probability >= threshold).astype(int)

# 12. Evaluation
print("\n========== MODEL PERFORMANCE ==========")

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, zero_division=0))
print("Recall:", recall_score(y_test, y_pred, zero_division=0))
print("F1 Score:", f1_score(y_test, y_pred, zero_division=0))
print("PR-AUC:", average_precision_score(y_test, y_probability))
print("ROC-AUC:", roc_auc_score(y_test, y_probability))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# 13. Save model and preprocessing objects
artifact = {
    "model": model,
    "encoder": encoder,
    "threshold": threshold,
    "numerical_columns": numerical_cols,
    "categorical_columns": categorical_cols,
    "feature_columns": X_train_final.columns.tolist()
}

joblib.dump(artifact, "bank_fraud_model.pkl")

print("\nModel saved successfully!")
print("File: bank_fraud_model.pkl")

print("\nTotal Training Time:", round(time.time() - start_time, 2), "seconds")
