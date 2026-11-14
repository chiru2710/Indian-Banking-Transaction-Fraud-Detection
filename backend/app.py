
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Create FastAPI app
app = FastAPI(title="FinGuard AI")

# Load trained model
artifact = joblib.load("model/bank_fraud_model.pkl")

model = artifact["model"]
encoder = artifact["encoder"]
threshold = artifact["threshold"]

numerical_cols = artifact["numerical_columns"]
categorical_cols = artifact["categorical_columns"]
feature_columns = artifact["feature_columns"]


# Transaction input
class Transaction(BaseModel):
    transaction_amount: float
    account_balance: float
    credit_score: int

    account_type: str
    transaction_type: str
    transaction_direction: str
    merchant_category: str
    state: str

    has_loan: int
    loan_type: str
    emi_amount: float

    transaction_status: str
    channel: str
    kyc_status: str

    transaction_hour: int
    transaction_date: str


# Home API
@app.get("/")
def home():
    return {"message": "FinGuard AI API is running"}


# Health API
@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}


# Fraud prediction API
@app.post("/predict")
def predict(transaction: Transaction):

    data = transaction.model_dump()

    df = pd.DataFrame([data])

    # Date feature engineering
    date = pd.to_datetime(df["transaction_date"])

    df["year"] = date.dt.year
    df["month"] = date.dt.month
    df["day"] = date.dt.day
    df["day_of_week"] = date.dt.dayofweek
    df["is_weekend"] = (date.dt.dayofweek >= 5).astype(int)

    # Loan handling
    if df.loc[0, "has_loan"] == 0:
        df.loc[0, "loan_type"] = "No Loan"
        df.loc[0, "emi_amount"] = 0

    # Numerical features
    numerical_data = df[numerical_cols]

    # Categorical encoding
    encoded = encoder.transform(df[categorical_cols])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(categorical_cols)
    )

    # Combine features
    final_data = pd.concat(
        [numerical_data.reset_index(drop=True), encoded_df],
        axis=1
    )

    final_data = final_data[feature_columns]

    # Prediction
    probability = model.predict_proba(final_data)[0][1]

    prediction = int(probability >= threshold)

    return {
        "prediction": prediction,
        "result": "Potential Fraud" if prediction == 1 else "Non-Fraud",
        "fraud_probability": round(probability * 100, 2),
        "threshold": threshold
    }
@app.get("/options")
def get_options():
    return {
        column: encoder.categories_[i].tolist()
        for i, column in enumerate(categorical_cols)
    }