
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
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

# 1. Load saved model
print("Loading trained model...")

artifact = joblib.load("bank_fraud_model.pkl")

model = artifact["model"]
encoder = artifact["encoder"]
threshold = artifact["threshold"]

numerical_cols = artifact["numerical_columns"]
categorical_cols = artifact["categorical_columns"]
feature_columns = artifact["feature_columns"]

print("Model loaded successfully!")

# 2. Load original dataset
print("\nLoading dataset...")

df = pd.read_csv("indian_banking_transactions.csv")

print("Dataset Shape:", df.shape)

# 3. Handle missing loan type
df.loc[
    (df["has_loan"] == 0) & (df["loan_type"].isna()),
    "loan_type"
] = "No Loan"

df.loc[
    (df["has_loan"] == 1) & (df["loan_type"].isna()),
    "loan_type"
] = "Unknown"

# 4. Extract date features
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

# 5. Drop unnecessary columns
df.drop(
    columns=[
        "transaction_id",
        "customer_id",
        "transaction_time",
        "transaction_date"
    ],
    inplace=True
)

# 6. Separate features and target
X = df.drop("is_fraud", axis=1)
y = df["is_fraud"]

# 7. Recreate the same train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTesting Data Shape:", X_test.shape)

# 8. Transform categorical features using saved encoder
X_test_encoded = encoder.transform(
    X_test[categorical_cols]
)

encoded_cols = encoder.get_feature_names_out(
    categorical_cols
)

# 9. Combine numerical and encoded features
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

# Ensure exact training feature order
X_test_final = X_test_final[feature_columns]

print("Final Testing Shape:", X_test_final.shape)

# 10. Predict
print("\nGenerating predictions...")

y_probability = model.predict_proba(
    X_test_final
)[:, 1]

y_pred = (y_probability >= threshold).astype(int)

# 11. Evaluate model
print("\n========== TEST RESULTS ==========")

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

print("\nTesting completed successfully!")
