import os
from datetime import date

import requests
import streamlit as st

# ============================================================
# FINGUARD AI - API CONFIGURATION
# ============================================================

API_URL = st.secrets.get(
    "FINGUARD_API_URL",
    os.getenv(
        "FINGUARD_API_URL",
        "https://indian-banking-transaction-fraud.onrender.com"
    )
).rstrip("/")

TIMEOUT = 30

REQUIRED_OPTIONS = [
    "account_type",
    "transaction_type",
    "transaction_direction",
    "merchant_category",
    "state",
    "loan_type",
    "transaction_status",
    "channel",
    "kyc_status",
]

# ============================================================
# WHITE CORPORATE GLASS CSS
# ============================================================

st.markdown(
    r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --black: #171717;
    --orange: #f47700;
    --orange-light: #ff9a32;
    --white: #ffffff;
    --muted: #555555;
    --line: rgba(35,35,35,.12);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    color: var(--black);
    background:
        radial-gradient(
            ellipse at 8% 0%,
            rgba(255,145,45,.18),
            transparent 34%
        ),
        radial-gradient(
            ellipse at 94% 15%,
            rgba(255,190,120,.16),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #f7f7f5 0%,
            #eeeeec 52%,
            #fafafa 100%
        );
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,.35);
}

.block-container {
    max-width: 1540px;
    padding-top: 1.55rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        rgba(255,255,255,.96),
        rgba(245,245,243,.98)
    );
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color: #222222;
}

h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: #171717 !important;
}

p, label, .stMarkdown {
    color: #343434;
}

.brand {
    font: 800 1.55rem 'Manrope';
    letter-spacing: -.055em;
    color: #171717;
}

.brand span {
    color: var(--orange);
}

.side-sub,
.eyebrow,
.section-kicker {
    color: #d96500;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-size: .67rem;
    font-weight: 800;
}

.side-status,
.glass-card,
.glass-panel,
.hero {
    border: 1px solid rgba(255,255,255,.9);
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.91),
        rgba(255,255,255,.66)
    );
    box-shadow:
        0 14px 38px rgba(25,25,25,.09),
        inset 0 1px 0 rgba(255,255,255,.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}

.side-status {
    margin-top: 1.35rem;
    padding: 15px;
    border-radius: 17px;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 31px 34px;
    border-radius: 25px;
    margin-bottom: 25px;
}

.hero:after {
    content: "";
    position: absolute;
    width: 290px;
    height: 290px;
    right: -95px;
    top: -150px;
    border-radius: 50%;
    background: rgba(255,121,0,.13);
    filter: blur(12px);
}

.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    color: #d96500;
    font-size: .7rem;
    letter-spacing: .13em;
    text-transform: uppercase;
    font-weight: 800;
}

.hero h1 {
    font-size: clamp(1.9rem,3.2vw,2.7rem) !important;
    letter-spacing: -.055em;
    margin: .55rem 0 .45rem;
    color: #171717 !important;
}

.hero p {
    max-width: 790px;
    color: #4b4b4b;
    margin: 0;
    line-height: 1.7;
}

.pulse {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--orange);
    box-shadow: 0 0 13px rgba(244,119,0,.55);
}

.section-title {
    font: 700 1.22rem 'Manrope';
    color: #171717;
    margin: 0 0 .22rem;
}

.section-copy,
.small-muted {
    font-size: .84rem;
    color: #555555;
}

.glass-card,
.glass-panel {
    border-radius: 19px;
    padding: 19px 20px;
}

.glass-card {
    min-height: 112px;
}

.glass-panel {
    border-radius: 21px;
    padding: 21px;
}

.glass-label {
    font-size: .67rem;
    letter-spacing: .13em;
    text-transform: uppercase;
    font-weight: 800;
    color: #666666;
}

.glass-value {
    font: 800 1.62rem 'Manrope';
    color: #171717;
    margin-top: 9px;
}

.glass-note {
    font-size: .74rem;
    color: #666666;
    margin-top: 4px;
}

div[data-testid="stForm"] {
    border: 1px solid rgba(255,255,255,.9);
    border-radius: 22px;
    padding: 22px;
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.92),
        rgba(255,255,255,.70)
    );
    box-shadow:
        0 16px 38px rgba(25,25,25,.08),
        inset 0 1px 0 #ffffff;
    backdrop-filter: blur(18px);
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
[data-testid="stDateInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,.95) !important;
    color: #171717 !important;
    border: 1px solid rgba(35,35,35,.18) !important;
    border-radius: 11px !important;
}

input, textarea {
    color: #171717 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #ffffff !important;
}

[role="option"] {
    color: #222222 !important;
}

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(
        120deg,
        #ff9a32,
        #f47700
    ) !important;
    color: #171717 !important;
    border: 1px solid rgba(255,255,255,.8) !important;
    border-radius: 12px !important;
    min-height: 48px;
    font-weight: 900;
    box-shadow:
        0 9px 22px rgba(244,119,0,.19),
        inset 0 1px 0 rgba(255,255,255,.55);
    transition: all .2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 13px 28px rgba(244,119,0,.27);
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,.80);
    border: 1px solid rgba(35,35,35,.10);
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,.05);
}

[data-testid="stMetricLabel"] {
    color: #555555 !important;
}

[data-testid="stMetricValue"] {
    color: #171717 !important;
}

.result-good,
.result-risk {
    border-radius: 21px;
    padding: 23px;
    margin-top: 10px;
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.95),
        rgba(255,255,255,.72)
    );
    border: 1px solid rgba(244,119,0,.35);
    box-shadow:
        0 14px 32px rgba(0,0,0,.07),
        inset 0 1px 0 #ffffff;
}

.result-risk {
    background: linear-gradient(
        145deg,
        rgba(255,244,233,.96),
        rgba(255,255,255,.82)
    );
    border-color: rgba(244,119,0,.55);
}

.result-title {
    font: 800 1.35rem 'Manrope';
    color: #171717;
}

.result-copy {
    color: #4b4b4b;
    margin-top: 7px;
    line-height: 1.6;
}

.prob-track {
    height: 11px;
    background: rgba(35,35,35,.10);
    border-radius: 20px;
    overflow: hidden;
    margin: 13px 0 7px;
}

.prob-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(
        90deg,
        #f47700,
        #ffb15c
    );
    box-shadow: 0 0 16px rgba(244,119,0,.22);
}

.risk-fill {
    background: linear-gradient(
        90deg,
        #f47700,
        #ffb15c
    );
}

.footer {
    text-align: center;
    color: #777777;
    font-size: .72rem;
    padding: 27px 0 8px;
}

hr {
    border-color: rgba(35,35,35,.13);
}

.stAlert {
    border-radius: 13px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def metric_card(label, value, note):
    st.markdown(
        f'<div class="glass-card">'
        f'<div class="glass-label">{label}</div>'
        f'<div class="glass-value">{value}</div>'
        f'<div class="glass-note">{note}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def section_header(number, title, description):
    st.markdown(
        f'<div class="section-kicker">'
        f'{number} / TRANSACTION MODULE</div>'
        f'<div class="section-title">{title}</div>'
        f'<div class="section-copy">{description}</div>',
        unsafe_allow_html=True,
    )


@st.cache_data(ttl=60, show_spinner=False)
def get_options(api_url):
    response = requests.get(
        f"{api_url}/options",
        timeout=TIMEOUT
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError(
            "The /options endpoint must return a JSON object."
        )

    return data


def api_health():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except (requests.RequestException, ValueError):
        return None


def predict(payload):
    response = requests.post(
        f"{API_URL}/predict",
        json=payload,
        timeout=TIMEOUT
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError(
            "The /predict endpoint did not return a JSON object."
        )

    return data


def parse_prediction(result):
    prediction_value = result.get(
        "prediction",
        result.get("is_fraud")
    )

    probability_value = result.get(
        "fraud_probability",
        result.get(
            "probability",
            result.get("fraud_prob")
        )
    )

    if prediction_value is None or probability_value is None:
        raise ValueError(
            "The API response must include prediction or is_fraud, "
            "and fraud_probability, probability or fraud_prob."
        )

    if isinstance(prediction_value, str):
        prediction = int(
            prediction_value.strip().lower()
            in {"1", "true", "fraud", "flagged"}
        )
    else:
        prediction = int(bool(prediction_value))

    probability = float(probability_value)
    threshold = float(result.get("threshold", 0.05))

    if probability > 1:
        probability /= 100

    if threshold > 1:
        threshold /= 100

    if not 0 <= probability <= 1:
        raise ValueError("Invalid fraud probability.")

    if not 0 <= threshold <= 1:
        raise ValueError("Invalid decision threshold.")

    return prediction, probability, threshold


# ============================================================
# DISPLAY PREDICTION RESULT
# ============================================================

def render_result(result, amount):
    prediction, probability, threshold = parse_prediction(result)

    probability_pct = probability * 100
    threshold_pct = threshold * 100

    st.markdown(
        '<div class="section-kicker">ANALYSIS COMPLETE</div>'
        '<div class="section-title">'
        'Transaction risk assessment</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Fraud probability",
            f"{probability_pct:.2f}%",
            "Model-estimated fraud score"
        )

    with col2:
        metric_card(
            "Decision threshold",
            f"{threshold_pct:.2f}%",
            "Configured classification cutoff"
        )

    with col3:
        metric_card(
            "Transaction value",
            f"₹{amount:,.2f}",
            "Submitted transaction amount"
        )

    if prediction:
        st.markdown(
            '<div class="result-risk">'
            '<div class="eyebrow">Elevated risk · Review required</div>'
            '<div class="result-title">'
            '⚠ Potentially suspicious transaction</div>'
            '<div class="result-copy">'
            'The model classified this transaction above its '
            'configured cutoff. Send it for independent verification. '
            'This output is not a final fraud determination.'
            '</div></div>',
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            '<div class="result-good">'
            '<div class="eyebrow">Below configured threshold</div>'
            '<div class="result-title">'
            '✓ Not flagged by the model</div>'
            '<div class="result-copy">'
            'The estimated score is below the configured cutoff. '
            'This does not guarantee that the transaction is legitimate.'
            '</div></div>',
            unsafe_allow_html=True,
        )

    fill_class = "risk-fill" if prediction else ""

    st.markdown(
        f'<div class="glass-panel" style="margin-top:16px">'
        f'<div style="display:flex;justify-content:space-between;gap:12px">'
        f'<span class="glass-label">Fraud probability score</span>'
        f'<strong style="color:#f47700">'
        f'{probability_pct:.2f}%</strong></div>'
        f'<div class="prob-track">'
        f'<div class="prob-fill {fill_class}" '
        f'style="width:{probability_pct:.2f}%"></div>'
        f'</div>'
        f'<div class="small-muted">'
        f'Decision threshold: {threshold_pct:.2f}%</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View raw API response"):
        st.json(result)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">FinGuard<span> AI</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-sub">'
        'BANKING TRANSACTION INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "WORKSPACE",
        ["Fraud Detection", "About Model"],
        label_visibility="visible"
    )

    st.markdown("---")

    health = api_health()

    if health and health.get("model_loaded", True):
        status = "API CONNECTED"
        detail = "Prediction service responding"

    elif health:
        status = "MODEL NOT READY"
        detail = "API online; model not confirmed"

    else:
        status = "API OFFLINE"
        detail = "Start FastAPI to enable analysis"

    st.markdown(
        f'<div class="side-status">'
        f'<div class="glass-label">SYSTEM STATUS</div>'
        f'<div style="margin:10px 0 5px;font-weight:800;color:#f47700">'
        f'● {status}</div>'
        f'<div style="font-size:.76rem;color:#555555">'
        f'{detail}</div>'
        f'<div style="font-size:.68rem;color:#666666;margin-top:12px">'
        f'Gradient Boosting · API mode</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="margin-top:27px;color:#777777;'
        'font-size:.68rem;line-height:1.9">'
        'FINGUARD AI<br>'
        'SECURE TRANSACTION ANALYTICS<br>'
        'CLIENT VERSION 3.0</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN HERO
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-tag">'
    '<span class="pulse"></span>'
    'Intelligent transaction monitoring</div>'
    '<h1>Banking Fraud Intelligence</h1>'
    '<p>Evaluate transaction risk through a connected '
    'machine-learning service. Review financial, account, '
    'payment-channel and customer-verification signals '
    'in one secure workspace.</p>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# LOAD OPTIONS FROM FASTAPI
# ============================================================

try:
    options = get_options(API_URL)

    missing = [
        key for key in REQUIRED_OPTIONS
        if key not in options or not options[key]
    ]

    if missing:
        st.error(
            "The API /options response is missing: "
            + ", ".join(missing)
        )
        st.stop()

except requests.RequestException as exc:
    st.error(
        f"Cannot connect to the FinGuard API at {API_URL}. "
        "Start FastAPI and refresh this page."
    )
    st.code(str(exc))
    st.stop()

except (ValueError, TypeError) as exc:
    st.error(f"Could not read dropdown options: {exc}")
    st.stop()


# ============================================================
# FRAUD DETECTION PAGE
# ============================================================

if page == "Fraud Detection":

    left, right = st.columns(
        [1.5, 0.78],
        gap="large"
    )

    # --------------------------------------------------------
    # TRANSACTION FORM
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">'
            'New transaction analysis</div>'
            '<div class="section-copy">'
            'Enter the transaction profile and submit it '
            'to the prediction API.</div>',
            unsafe_allow_html=True,
        )

        with st.form(
            "finguard_transaction_form",
            clear_on_submit=False
        ):

            # 01 Financial profile

            section_header(
                "01",
                "Financial profile",
                "Transaction value and customer financial indicators."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                transaction_amount = st.number_input(
                    "Transaction amount (₹)",
                    min_value=0.0,
                    value=5000.0,
                    step=500.0
                )

            with c2:
                account_balance = st.number_input(
                    "Account balance (₹)",
                    min_value=0.0,
                    value=25000.0,
                    step=1000.0
                )

            with c3:
                credit_score = st.number_input(
                    "Credit score",
                    min_value=300,
                    max_value=900,
                    value=700
                )

            st.markdown("---")

            # 02 Account profile

            section_header(
                "02",
                "Account profile",
                "Account type, loan status and repayment information."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                account_type = st.selectbox(
                    "Account type",
                    options["account_type"]
                )

            with c2:
                has_loan = st.selectbox(
                    "Existing loan",
                    [0, 1],
                    format_func=lambda value:
                        "Yes" if value else "No"
                )

            with c3:
                emi_amount = st.number_input(
                    "EMI amount (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=500.0
                )

            loan_type = st.selectbox(
                "Loan type",
                options["loan_type"],
                disabled=(has_loan == 0)
            )

            st.markdown("---")

            # 03 Transaction behaviour

            section_header(
                "03",
                "Transaction behaviour",
                "Payment method, direction, merchant and transaction channel."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                transaction_type = st.selectbox(
                    "Transaction type",
                    options["transaction_type"]
                )

            with c2:
                transaction_direction = st.selectbox(
                    "Transaction direction",
                    options["transaction_direction"]
                )

            with c3:
                merchant_category = st.selectbox(
                    "Merchant category",
                    options["merchant_category"]
                )

            c1, c2, c3 = st.columns(3)

            with c1:
                transaction_status = st.selectbox(
                    "Transaction status",
                    options["transaction_status"]
                )

            with c2:
                channel = st.selectbox(
                    "Transaction channel",
                    options["channel"]
                )

            with c3:
                transaction_hour = st.slider(
                    "Transaction hour",
                    0,
                    23,
                    12,
                    format="%d:00"
                )

            st.markdown("---")

            # 04 Customer verification

            section_header(
                "04",
                "Customer verification",
                "Geographic and KYC context for the transaction."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                state = st.selectbox(
                    "State",
                    options["state"]
                )

            with c2:
                kyc_status = st.selectbox(
                    "KYC status",
                    options["kyc_status"]
                )

            with c3:
                transaction_date = st.date_input(
                    "Transaction date",
                    value=date.today()
                )

            st.markdown(
                "<div style='height:8px'></div>",
                unsafe_allow_html=True
            )

            submitted = st.form_submit_button(
                "◈  ANALYZE TRANSACTION",
                use_container_width=True
            )

    # --------------------------------------------------------
    # RIGHT SIDE DASHBOARD PANELS
    # --------------------------------------------------------

    with right:

        # Prediction workflow

        st.markdown(
            '<div class="glass-panel">'
            '<div class="eyebrow">Prediction workflow</div>'
            '<div class="section-title" style="margin-top:8px">'
            'From input to insight</div>'
            '<p class="small-muted">'
            'The Streamlit interface sends your transaction '
            'to the existing FastAPI service.</p>'

            '<div style="margin-top:20px;color:#f47700;font-weight:800">'
            '01 · Input validation</div>'
            '<div class="small-muted">'
            'Review financial and account fields.</div>'

            '<div style="margin-top:17px;color:#f47700;font-weight:800">'
            '02 · Model inference</div>'
            '<div class="small-muted">'
            'The backend applies the saved encoder and '
            'Gradient Boosting model.</div>'

            '<div style="margin-top:17px;color:#f47700;font-weight:800">'
            '03 · Risk assessment</div>'
            '<div class="small-muted">'
            'The model score is compared with the configured '
            'decision threshold.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='height:14px'></div>",
            unsafe_allow_html=True
        )

        # Responsible use

        st.markdown(
            '<div class="glass-panel">'
            '<div class="eyebrow">Responsible use</div>'
            '<div style="font:700 1rem Manrope;color:#171717;'
            'margin:8px 0">A risk signal, not a final verdict</div>'
            '<div class="small-muted">'
            'Use this score to support an initial review only. '
            'Before taking action, verify the transaction context, '
            'check the customer history and confirm unusual activity '
            'through an independently verified contact channel. '
            'Never approve, block or accuse a customer based only '
            'on this model output.'
            '</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='height:14px'></div>",
            unsafe_allow_html=True
        )

        # Review checklist

        st.markdown(
            '<div class="glass-panel">'
            '<div class="eyebrow">Review checklist</div>'
            '<div class="section-title" style="margin-top:8px">'
            'Signals worth checking</div>'

            '<div style="margin-top:15px;color:#f47700;font-weight:800">'
            '01 · Amount and balance</div>'
            '<div class="small-muted">'
            'Compare the transaction amount with the available '
            'balance and the customer’s usual activity.</div>'

            '<div style="margin-top:13px;color:#f47700;font-weight:800">'
            '02 · Payment behaviour</div>'
            '<div class="small-muted">'
            'Review the payment channel, transaction type, direction, '
            'merchant category and time.</div>'

            '<div style="margin-top:13px;color:#f47700;font-weight:800">'
            '03 · Account context</div>'
            '<div class="small-muted">'
            'Check account type, loan details, KYC status and whether '
            'the transaction information is complete.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='height:14px'></div>",
            unsafe_allow_html=True
        )

        # Score explanation

        st.markdown(
            '<div class="glass-panel">'
            '<div class="eyebrow">How to read the score</div>'
            '<div class="section-title" style="margin-top:8px">'
            'Probability versus threshold</div>'
            '<div class="small-muted" style="margin-top:9px">'
            'The probability is the model-estimated fraud score. '
            'The threshold is the configured cutoff used to produce '
            'the model’s flagged or not-flagged result. A score below '
            'the cutoff does not guarantee a safe transaction.'
            '</div></div>',
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # SUBMIT TO FASTAPI /predict
    # --------------------------------------------------------

    if submitted:

        if transaction_amount <= 0:
            st.error(
                "Transaction amount must be greater than zero."
            )

        elif has_loan == 0 and emi_amount != 0:
            st.error(
                "EMI amount should be zero when no loan exists."
            )

        elif has_loan == 1 and emi_amount <= 0:
            st.error(
                "Please enter a valid EMI amount for the existing loan."
            )

        else:

            payload = {
                "transaction_amount": float(transaction_amount),
                "account_balance": float(account_balance),
                "credit_score": int(credit_score),
                "account_type": account_type,
                "has_loan": int(has_loan),
                "loan_type": (
                    "No Loan" if has_loan == 0 else loan_type
                ),
                "emi_amount": (
                    0.0 if has_loan == 0 else float(emi_amount)
                ),
                "transaction_type": transaction_type,
                "transaction_direction": transaction_direction,
                "merchant_category": merchant_category,
                "transaction_status": transaction_status,
                "channel": channel,
                "transaction_hour": int(transaction_hour),
                "state": state,
                "kyc_status": kyc_status,
                "transaction_date": transaction_date.isoformat(),
            }

            with st.spinner("Analyzing transaction signals..."):

                try:
                    st.session_state["last_prediction"] = predict(
                        payload
                    )

                    st.session_state["last_amount"] = (
                        transaction_amount
                    )

                except requests.HTTPError as exc:
                    st.error(
                        "The prediction API returned an HTTP error."
                    )

                    st.code(
                        exc.response.text
                        if exc.response is not None
                        else str(exc)
                    )

                except requests.RequestException as exc:
                    st.error(
                        "Could not reach the prediction service."
                    )
                    st.code(str(exc))

                except (ValueError, TypeError) as exc:
                    st.error(
                        f"Unexpected prediction response: {exc}"
                    )

    # Display previous prediction

    if "last_prediction" in st.session_state:

        st.markdown("---")

        try:
            render_result(
                st.session_state["last_prediction"],
                st.session_state.get("last_amount", 0.0)
            )

        except (ValueError, TypeError) as exc:
            st.error(
                f"Could not display the prediction result: {exc}"
            )
            st.json(st.session_state["last_prediction"])


# ============================================================
# ABOUT MODEL PAGE
# ============================================================

elif page == "About Model":

    st.markdown(
        '<div class="section-kicker">MODEL INTELLIGENCE</div>'
        '<div class="section-title">'
        'Model overview & evaluation</div>'
        '<div class="section-copy">'
        'Recorded test-set metrics for the current project model.'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        metric_card(
            "Algorithm",
            "Gradient Boosting",
            "Supervised binary classification"
        )

    with c2:
        metric_card(
            "Decision threshold",
            "5.00%",
            "Configured classification cutoff"
        )

    st.markdown(
        "<div style='height:14px'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Recorded test metrics</div>',
        unsafe_allow_html=True,
    )

    metrics = [
        ("Accuracy", "98.22%", "Overall correct predictions"),
        ("Precision", "8.28%", "Flagged transactions that were fraud"),
        ("Recall", "10.05%", "Actual fraud cases detected"),
        ("F1 score", "9.08%", "Precision-recall balance"),
        ("PR-AUC", "0.01955", "Precision-recall area"),
        ("ROC-AUC", "0.54293", "ROC discrimination score"),
    ]

    cols = st.columns(3)

    for index, (name, value, note) in enumerate(metrics):
        with cols[index % 3]:
            metric_card(name, value, note)

    st.markdown(
        "<div style='height:14px'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-risk">'
        '<div class="eyebrow">Model limitation</div>'
        '<div class="result-title">'
        'Not production-ready for real banking decisions</div>'
        '<div class="result-copy">'
        'Although accuracy is high, fraud-class precision and recall '
        'are low. The recorded recall of approximately 10.05% means '
        'the model misses many actual fraud cases. Treat predictions '
        'as an educational demonstration and require independent review.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    with st.expander("Technical configuration"):
        st.write(
            "**Model family:** Gradient Boosting Classifier"
        )
        st.write("**Frontend:** Streamlit")
        st.write("**Backend:** FastAPI")
        st.write("**Inference route:** `POST /predict`")
        st.write("**Dropdown route:** `GET /options`")
        st.write(
            "**Feature preparation:** "
            "Performed by the backend service"
        )
        st.write(f"**API base URL:** `{API_URL}`")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'FINGUARD AI&nbsp; · &nbsp;BANKING TRANSACTION INTELLIGENCE<br>'
    'Built with Streamlit · FastAPI · Python · Scikit-learn'
    '</div>',
    unsafe_allow_html=True,
)
