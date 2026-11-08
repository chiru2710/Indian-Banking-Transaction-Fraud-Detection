
import streamlit as st
import pandas as pd
import joblib
from datetime import date

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FinGuard AI | Fraud Detection",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    background: #101c35;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
    padding: 12px 0 4px 0;
}

.brand span {
    color: #38bdf8;
}

.sidebar-caption {
    color: #a8b5cc !important;
    font-size: 12px;
    margin-bottom: 25px;
}

.sidebar-status {
    background: #1c2c49;
    padding: 14px;
    border-radius: 12px;
    margin-top: 25px;
    font-size: 13px;
}

.hero {
    background: linear-gradient(115deg, #132849, #174b79);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #d4e6f7;
    font-size: 14px;
    margin-bottom: 0;
}

.section-heading {
    font-size: 20px;
    font-weight: 750;
    color: #14243d;
    margin: 20px 0 14px 0;
}

.metric-card {
    background: white;
    border: 1px solid #e5eaf2;
    padding: 20px;
    border-radius: 15px;
    min-height: 115px;
    box-shadow: 0 3px 12px rgba(20, 40, 70, 0.04);
}

.metric-label {
    color: #718096;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .6px;
}

.metric-value {
    color: #14243d;
    font-size: 25px;
    font-weight: 800;
    margin-top: 10px;
}

.metric-note {
    color: #8492a6;
    font-size: 11px;
    margin-top: 4px;
}

.form-card {
    background: white;
    border: 1px solid #e5eaf2;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 15px;
}

div[data-testid="stForm"] {
    background: white;
    padding: 24px;
    border: 1px solid #e5eaf2;
    border-radius: 16px;
}

.stButton > button,
.stFormSubmitButton > button {
    background: #1769aa;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 700;
    min-height: 48px;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #10558c;
    color: white;
}

.result-card {
    background: white;
    border: 1px solid #e5eaf2;
    border-radius: 16px;
    padding: 25px;
    margin-top: 18px;
}

.success-result {
    border-left: 6px solid #16a36a;
}

.danger-result {
    border-left: 6px solid #dc4545;
}

.result-title {
    font-size: 22px;
    font-weight: 800;
    color: #14243d;
}

.result-description {
    color: #64748b;
    font-size: 14px;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5eaf2;
    padding: 16px;
    border-radius: 13px;
}

hr {
    border-color: #e5eaf2;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    padding: 25px 0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("bank_fraud_model.pkl")

try:
    artifact = load_model()

    model = artifact["model"]
    encoder = artifact["encoder"]
    threshold = artifact["threshold"]

    numerical_cols = artifact["numerical_columns"]
    categorical_cols = artifact["categorical_columns"]
    feature_columns = artifact["feature_columns"]

except Exception as e:
    st.error(f"Unable to load model: {e}")
    st.stop()

# ==========================================
# 4. SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        '<div class="brand">FinGuard<span> AI</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-caption">INTELLIGENT FRAUD MONITORING</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        ["Fraud Detection", "About Model"],
        label_visibility="visible"
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="sidebar-status">
            <b>● Model Status: Loaded</b><br><br>
            <span style="color:#a8b5cc">
            Gradient Boosting Classifier<br>
            Prediction Engine Active
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="margin-top:35px;color:#a8b5cc;font-size:11px">
        FINGUARD AI<br>
        Banking Fraud Intelligence<br>
        Version 1.0.0
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 5. HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
    <h1>Banking Fraud Intelligence</h1>
    <p>Analyze transaction patterns and identify potentially
    fraudulent banking activities using machine learning.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. FRAUD DETECTION PAGE
# ==========================================

if page == "Fraud Detection":

    st.markdown(
        '<div class="section-heading">Transaction Analysis</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter the transaction information below to generate "
        "an AI-based risk assessment."
    )

    with st.form("fraud_detection_form"):

        st.markdown("### 01. Financial Information")

        c1, c2, c3 = st.columns(3)

        with c1:
            transaction_amount = st.number_input(
                "Transaction Amount (₹)",
                min_value=0.0,
                value=5000.0,
                step=500.0
            )

        with c2:
            account_balance = st.number_input(
                "Account Balance (₹)",
                min_value=0.0,
                value=25000.0,
                step=1000.0
            )

        with c3:
            credit_score = st.number_input(
                "Credit Score",
                min_value=300,
                max_value=900,
                value=700
            )

        st.markdown("---")
        st.markdown("### 02. Account Information")

        c1, c2, c3 = st.columns(3)

        with c1:
            account_type = st.selectbox(
                "Account Type",
                encoder.categories_[
                    categorical_cols.index("account_type")
                ].tolist()
            )

        with c2:
            has_loan = st.selectbox(
                "Existing Loan",
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No"
            )

        with c3:
            emi_amount = st.number_input(
                "EMI Amount (₹)",
                min_value=0.0,
                value=0.0,
                step=500.0
            )

        loan_options = encoder.categories_[
            categorical_cols.index("loan_type")
        ].tolist()

        loan_type = st.selectbox(
            "Loan Type",
            loan_options,
            disabled=(has_loan == 0)
        )

        st.markdown("---")
        st.markdown("### 03. Transaction Information")

        c1, c2, c3 = st.columns(3)

        with c1:
            transaction_type = st.selectbox(
                "Transaction Type",
                encoder.categories_[
                    categorical_cols.index("transaction_type")
                ].tolist()
            )

        with c2:
            transaction_direction = st.selectbox(
                "Transaction Direction",
                encoder.categories_[
                    categorical_cols.index("transaction_direction")
                ].tolist()
            )

        with c3:
            merchant_category = st.selectbox(
                "Merchant Category",
                encoder.categories_[
                    categorical_cols.index("merchant_category")
                ].tolist()
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            transaction_status = st.selectbox(
                "Transaction Status",
                encoder.categories_[
                    categorical_cols.index("transaction_status")
                ].tolist()
            )

        with c2:
            channel = st.selectbox(
                "Transaction Channel",
                encoder.categories_[
                    categorical_cols.index("channel")
                ].tolist()
            )

        with c3:
            transaction_hour = st.slider(
                "Transaction Hour",
                0, 23, 12
            )

        st.markdown("---")
        st.markdown("### 04. Customer Verification")

        c1, c2, c3 = st.columns(3)

        with c1:
            state = st.selectbox(
                "State",
                encoder.categories_[
                    categorical_cols.index("state")
                ].tolist()
            )

        with c2:
            kyc_status = st.selectbox(
                "KYC Status",
                encoder.categories_[
                    categorical_cols.index("kyc_status")
                ].tolist()
            )

        with c3:
            transaction_date = st.date_input(
                "Transaction Date",
                value=date.today()
            )

        st.markdown("<br>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "Analyze Transaction",
            use_container_width=True
        )

    # ==========================================
    # 7. PREDICTION
    # ==========================================

    if submitted:

        if transaction_amount <= 0:
            st.error("Transaction amount must be greater than zero.")

        elif has_loan == 0 and emi_amount != 0:
            st.error("EMI amount should be zero when no loan exists.")

        elif has_loan == 1 and emi_amount == 0:
            st.warning("Please verify the EMI amount for this loan.")

        else:

            if has_loan == 0:
                loan_type = "No Loan"
                emi_amount = 0.0

            input_data = {
                "transaction_amount": transaction_amount,
                "account_balance": account_balance,
                "credit_score": credit_score,
                "has_loan": has_loan,
                "emi_amount": emi_amount,
                "transaction_hour": transaction_hour,
                "year": transaction_date.year,
                "month": transaction_date.month,
                "day": transaction_date.day,
                "day_of_week": transaction_date.weekday(),
                "is_weekend": int(transaction_date.weekday() >= 5),
                "account_type": account_type,
                "transaction_type": transaction_type,
                "transaction_direction": transaction_direction,
                "merchant_category": merchant_category,
                "state": state,
                "loan_type": loan_type,
                "transaction_status": transaction_status,
                "channel": channel,
                "kyc_status": kyc_status
            }

            input_df = pd.DataFrame([input_data])

            input_df = input_df[
                numerical_cols + categorical_cols
            ]

            encoded_data = encoder.transform(
                input_df[categorical_cols]
            )

            encoded_cols = encoder.get_feature_names_out(
                categorical_cols
            )

            encoded_df = pd.DataFrame(
                encoded_data,
                columns=encoded_cols
            )

            final_input = pd.concat(
                [
                    input_df[numerical_cols].reset_index(drop=True),
                    encoded_df
                ],
                axis=1
            )

            final_input = final_input[feature_columns]

            probability = model.predict_proba(
                final_input
            )[0][1]

            prediction = int(probability >= threshold)

            # ==================================
            # 8. RESULTS DASHBOARD
            # ==================================

            st.markdown("---")

            st.markdown(
                '<div class="section-heading">Risk Assessment Report</div>',
                unsafe_allow_html=True
            )

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "Fraud Probability",
                    f"{probability * 100:.2f}%"
                )

            with m2:
                st.metric(
                    "Decision Threshold",
                    f"{threshold * 100:.0f}%"
                )

            with m3:
                st.metric(
                    "Transaction Amount",
                    f"₹{transaction_amount:,.2f}"
                )

            if prediction == 1:

                st.markdown("""
                <div class="result-card danger-result">
                    <div class="result-title">
                        ⚠ Potential Fraud Detected
                    </div>
                    <p class="result-description">
                        The machine learning model has classified
                        this transaction as potentially fraudulent.
                        Further verification is recommended.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.error("Risk status: Flagged for manual review")

            else:

                st.markdown("""
                <div class="result-card success-result">
                    <div class="result-title">
                        ✓ Classified as Legitimate
                    </div>
                    <p class="result-description">
                        The model probability is below the configured
                        fraud detection threshold.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.success("Risk status: Not flagged by the model")

            st.markdown("#### Fraud Probability Distribution")

            st.progress(float(probability))

            st.caption(
                "Probability is the model's estimated fraud score, "
                "not a calibrated guarantee of actual fraud."
            )

            with st.expander("View transaction details"):
                st.dataframe(
                    pd.DataFrame([input_data]),
                    use_container_width=True,
                    hide_index=True
                )

# ==========================================
# 9. ABOUT MODEL PAGE
# ==========================================

elif page == "About Model":

    st.markdown(
        '<div class="section-heading">Model Information</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Algorithm</div>
            <div class="metric-value">Gradient Boosting</div>
            <div class="metric-note">Supervised classification</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Decision Threshold</div>
            <div class="metric-value">{threshold:.2f}</div>
            <div class="metric-note">Configured classification threshold</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Model Test Metrics")

    metrics = {
        "Accuracy": "98.22%",
        "Precision": "8.28%",
        "Recall": "10.05%",
        "F1 Score": "9.08%",
        "PR-AUC": "0.01955",
        "ROC-AUC": "0.54293"
    }

    cols = st.columns(3)

    for i, (name, value) in enumerate(metrics.items()):
        with cols[i % 3]:
            st.metric(name, value)

    st.warning(
        "The model currently has limited fraud detection capability. "
        "Its test recall is approximately 10.05%, meaning it misses "
        "many actual fraud cases. This application is a demonstration "
        "and should not be used for real banking decisions."
    )

# ==========================================
# 10. FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    FinGuard AI • Banking Fraud Intelligence • ML Project<br>
    Built with Python, Scikit-learn and Streamlit
</div>
""", unsafe_allow_html=True)
