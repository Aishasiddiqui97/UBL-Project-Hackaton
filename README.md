# AFCIP — Anti Financial Crime Investigation Platform
## AI/ML Fraud Detection & Risk Scoring Engine

A production-ready AI/ML module that receives financial transaction data,
predicts fraud probability using a Random Forest model, calculates a risk
score using business rules, and returns a structured JSON response via FastAPI.

---

## Project Overview

| Component | Description |
|---|---|
| **Dataset** | 5,000 synthetic transactions (85% normal / 15% fraud) |
| **Model** | RandomForestClassifier (scikit-learn) |
| **API** | FastAPI REST endpoint with Pydantic validation |
| **Risk Engine** | Rule-based scoring system capped at 100 points |

### Risk Scoring Rules

| Condition | Points |
|---|---|
| Amount > 500,000 | +40 |
| Transaction Count > 10 | +30 |
| New Location | +20 |
| Fraud Probability > 80% | +10 |
| **Maximum** | **100** |

### Risk Levels

| Score Range | Level |
|---|---|
| 0 – 30 | Low Risk |
| 31 – 70 | Medium Risk |
| 71 – 100 | High Risk |

---

## Project Structure

```
ai_ml/
├── dataset/
│   ├── generate_dataset.py     # Generates transactions.csv
│   └── transactions.csv        # Generated dataset (5,000 records)
├── fraud_detection/
│   ├── __init__.py
│   ├── data_preprocessing.py   # Load, clean, encode, split data
│   ├── train_model.py          # Train RandomForest, save model.pkl
│   ├── predict.py              # predict_transaction() function
│   ├── model.pkl               # Trained model (created after training)
│   └── encoder.pkl             # Label encoders (created after training)
├── risk_scoring/
│   ├── __init__.py
│   ├── rules.py                # Business rule definitions
│   └── scoring.py              # Risk score calculation
├── api/
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Shared utility functions
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.12+
- pip

### Step 1 — Clone / Navigate to the project

```bash
cd "AFCIP AI"
```

### Step 2 — Create a Virtual Environment

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

All commands must be run from the **project root** (`AFCIP AI/`).

### Step 1 — Generate Dataset

```bash
python dataset/generate_dataset.py
```

Expected output:
```
INFO: Dataset saved → dataset/transactions.csv
INFO: Total records  : 5000
INFO: Normal (0)     : 4250
INFO: Fraud  (1)     : 750
```

### Step 2 — Train the Model

```bash
python -m fraud_detection.train_model
```

Expected output:
```
==================================================
       MODEL EVALUATION METRICS
==================================================
  Accuracy  : 97.xx%
  Precision : 95.xx%
  Recall    : 94.xx%
  F1 Score  : 94.xx%
==================================================
```

This creates:
- `fraud_detection/model.pkl`
- `fraud_detection/encoder.pkl`

### Step 3 — Start the FastAPI Server

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## API Reference

### Health Check

```
GET /
```

**Response:**
```json
{
  "status": "ok",
  "service": "AFCIP AI/ML Engine"
}
```

---

### Analyze Transaction

```
POST /analyze-transaction
```

#### Request Headers

```
Content-Type: application/json
```

#### Request Body Schema

| Field | Type | Required | Validation |
|---|---|---|---|
| account_no | string | ✅ | Non-empty |
| amount | float | ✅ | > 0 |
| location | string | ✅ | Non-empty |
| transaction_count | int | ✅ | >= 0 |
| transaction_type | string | ✅ | Non-empty |
| device_type | string | ✅ | Non-empty |
| is_new_location | bool | ✅ | true / false |

---

## Sample Requests & Responses

### Example 1 — High Risk Fraud Transaction

**Request:**
```json
{
  "account_no": "1002",
  "amount": 850000,
  "location": "Islamabad",
  "transaction_count": 17,
  "transaction_type": "Transfer",
  "device_type": "Mobile",
  "is_new_location": true
}
```

**Response:**
```json
{
  "fraud_probability": 92,
  "prediction": "Fraud",
  "risk_score": 100,
  "status": "High Risk"
}
```

---

### Example 2 — Low Risk Normal Transaction

**Request:**
```json
{
  "account_no": "3041",
  "amount": 15000,
  "location": "Karachi",
  "transaction_count": 3,
  "transaction_type": "Payment",
  "device_type": "Desktop",
  "is_new_location": false
}
```

**Response:**
```json
{
  "fraud_probability": 8,
  "prediction": "Normal",
  "risk_score": 0,
  "status": "Low Risk"
}
```

---

### Example 3 — Medium Risk Transaction

**Request:**
```json
{
  "account_no": "5523",
  "amount": 250000,
  "location": "Lahore",
  "transaction_count": 12,
  "transaction_type": "Withdrawal",
  "device_type": "ATM",
  "is_new_location": true
}
```

**Response:**
```json
{
  "fraud_probability": 55,
  "prediction": "Fraud",
  "risk_score": 50,
  "status": "Medium Risk"
}
```

---

### cURL Examples

```bash
# High risk transaction
curl -X POST "http://localhost:8000/analyze-transaction" \
  -H "Content-Type: application/json" \
  -d '{
    "account_no": "1002",
    "amount": 850000,
    "location": "Islamabad",
    "transaction_count": 17,
    "transaction_type": "Transfer",
    "device_type": "Mobile",
    "is_new_location": true
  }'
```

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12 | Core language |
| FastAPI | 0.115.x | REST API framework |
| Uvicorn | 0.34.x | ASGI server |
| scikit-learn | 1.6.x | ML model (RandomForest) |
| Pandas | 2.2.x | Data loading & manipulation |
| NumPy | 2.2.x | Numerical operations |
| Joblib | 1.4.x | Model serialization |
| Pydantic | 2.11.x | Request/response validation |

---

## Step-by-Step Quick Start

```bash
# 1. Navigate to project root
cd "AFCIP AI"

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows CMD
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate dataset
python dataset/generate_dataset.py

# 5. Train the model
python -m fraud_detection.train_model

# 6. Start the API server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 7. Open browser → http://localhost:8000/docs
```

---

## License

MIT License — For educational and research purposes.
