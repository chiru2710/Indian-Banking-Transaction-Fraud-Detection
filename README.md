# FinGuard AI – Indian Banking Transaction Fraud Detection

An end-to-end Machine Learning project that analyzes banking transactions and predicts potentially fraudulent activities using classification techniques.

## Project Overview

FinGuard AI is a machine learning-based fraud detection application designed to identify suspicious banking transactions. It uses transaction details, customer account information, merchant categories, and transaction channels to estimate the probability of fraud.

The project includes model training, evaluation, and an interactive Streamlit application.

## Key Features

- Banking transaction data preprocessing
- Handling missing values and categorical variables
- Imbalanced dataset analysis
- Gradient Boosting classification model
- Fraud probability prediction
- Custom classification threshold
- Model evaluation using classification metrics
- Interactive Streamlit dashboard

## Technology Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Model Storage:** Joblib
- **Web Application:** Streamlit
- **Version Control:** Git and GitHub

## Dataset Information

| Description | Value |
|---|---:|
| Total Transactions | 550,000 |
| Total Features | 20 |
| Fraud Transactions | 4,873 |
| Non-Fraud Transactions | 545,127 |
| Fraud Percentage | 0.89% |
| Non-Fraud Percentage | 99.11% |

**Target Variable:** `is_fraud`

- `0` – Non-Fraudulent Transaction
- `1` – Fraudulent Transaction

*Note: The dataset is used for this project and its source and real-world authenticity have not been independently verified.*

## Machine Learning Model

**Algorithm:** Gradient Boosting Classifier

The model uses preprocessing and feature encoding before training. The classification threshold is set to 0.05 in the current training configuration.

### Model Performance

| Metric | Score |
|---|---:|
| Accuracy | 98.22% |
| Precision | 8.28% |
| Recall | 10.05% |
| F1 Score | 9.08% |
| PR-AUC | 0.01955 |
| ROC-AUC | 0.54293 |

**Important:** Although accuracy is high, fraud detection performance is currently weak. The low precision, recall, and PR-AUC indicate that the model needs further improvement before any real banking use. Accuracy alone is not a reliable measure for this highly imbalanced dataset.

## Project Structure

```text
finguard-ai-banking-fraud-detection/
│
├── app.py
├── train.py
├── test.py
├── requirements.txt
├── bank_fraud_model.pkl
├── .gitignore
└── README.md
```

The original CSV dataset is not included in the repository.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/finguard-ai-banking-fraud-detection.git
```

### 2. Navigate to the project folder

```bash
cd finguard-ai-banking-fraud-detection
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Dataset Setup

Place the dataset file in the project root directory:

```text
indian_banking_transactions.csv
```

The CSV file is required to train and evaluate the model. It is excluded from GitHub through `.gitignore`.

## Model Training

Run:

```bash
python train.py
```

This script preprocesses the dataset, trains the Gradient Boosting model, evaluates its performance, and saves the trained model as:

```text
bank_fraud_model.pkl
```

## Model Testing

Run:

```bash
python test.py
```

This evaluates the saved model using the test split.

## Run the Streamlit Application

Run:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal to access the FinGuard AI application.

## Deployment

The application can be deployed using [Streamlit Community Cloud](https://share.streamlit.io/).

Select your GitHub repository and set the main file path to:

```text
app.py
```

Ensure the trained model file is available to the deployed application.

## Future Improvements

- Improve fraud detection precision and recall
- Experiment with XGBoost, LightGBM, and other ensemble models
- Apply cost-sensitive learning techniques
- Optimize classification thresholds using validation data
- Perform cross-validation and hyperparameter tuning
- Add explainable AI using SHAP
- Explore real-time transaction monitoring

## Disclaimer

FinGuard AI is an educational machine learning project. Its predictions are experimental and should not be used to approve, reject, or block actual banking transactions.

## Author

**Jangili Ch M Srinivasa Vara Prasad**

- GitHub: [chiru2710](https://github.com/chiru2710)
- LinkedIn: [Connect on LinkedIn](https://www.linkedin.com/in/jangili-ch-m-srinivasa-vara-prasad-213097315/)

---

*FinGuard AI – Exploring Machine Learning for Banking Fraud Detection.*