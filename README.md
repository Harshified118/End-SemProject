# 👟 DropOrCop: Sneaker & Streetwear Resale Profit Predictor

> A machine-learning valuation engine that predicts resale prices and profit margins for limited-edition sneakers to provide an instant **COP (buy)** or **DROP (skip)** verdict.

---

## 👥 Team Members (Group G)

| Sl. No. | Name | Role & Responsibility |
|:---:|:---|:---|
| **31** | **Harsh Kumar** *(Team Leader)* | **ML Lead:** Data Ingestion, Feature Preprocessing & Model Training (Phases 1–3) |
| **32** | **Anamika Ghosh** | **Evaluation Lead:** Model Evaluation, Error Metrics (MAE/MAPE) & Diagnostics (Phase 4) |
| **33** | *(Sl. No. 33)* | **Data & Testing:** Exploratory Data Analysis Support & Integration Testing |
| **34** | **Sinthoiba Kangjam** | **API & Backend Lead:** FastAPI Service (`/predict`, `/health`) (Phase 5) |
| **35** | **Himesh Vaskar** | **Frontend Lead:** User Interface, Input Controls & Verdict Display (Phase 6) |

---

## 💡 Overview

Limited-edition sneaker prices fluctuate dramatically on the secondary market (StockX, GOAT). **DropOrCop** removes the guesswork:
- **Trained on historical secondary market transactions** (Nike x Off-White, Adidas Yeezy).
- **Predicts resale prices** based on brand, retail price, shoe size, and days since release.
- **Calculates expected profit:** $\text{Profit} = \text{Predicted Resale Price} - \text{Retail Price}$.
- **Delivers a verdict:**
  - 🟢 **COP**: Profitable resale margin above threshold.
  - 🔴 **DROP**: Low or negative margin.

---

## 🏗 System Architecture

```text
Historical Sales Data (StockX)
         │
         ▼
[Phase 1 & 2: src/data_prep.py] ── Clean & engineer features (days_since_release)
         │
         ▼
[Phase 3: src/train.py] ────────── Train RandomForestRegressor -> models/best_model.joblib
         │
         ├───▶ [Phase 4: Evaluation] ── Test predictions & diagnostics (MAPE/MAE)
         │
         ▼
[Phase 5: api/main.py] ─────────── FastAPI REST API (/predict)
         │
         ▼
[Phase 6: frontend/] ───────────── Interactive Web UI with COP/DROP badge
```

---

## 📁 Repository Structure

```text
├── data/
│   ├── raw/               # Raw transaction datasets (StockX)
│   └── processed/         # Cleaned data & evaluation predictions
├── models/                # Serialized model pipelines (.joblib)
├── src/                   # Core ML scripts (data_prep, train, predict)
├── api/                   # FastAPI backend service
├── frontend/              # Web interface
├── requirements.txt       # Project dependencies
└── README.md
```

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Data Preparation & Training
```bash
# Clean raw transaction data
python src/data_prep.py

# Train regression model & export pipeline
python src/train.py
```

### 3. Run API & Frontend
```bash
# Start FastAPI backend
uvicorn api.main:app --reload

# Open frontend/index.html in a web browser
```

---

## 📄 License
Academic Project – B.Tech CSE End-Semester Assessment (November 2026).
