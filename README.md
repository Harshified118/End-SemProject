# 👟 DropOrCop: Sneaker & Streetwear Resale Profit Predictor

> A machine-learning valuation application that estimates resale prices and profit margins for limited-edition sneakers to provide an immediate **COP (buy)** or **DROP (skip)** verdict.  
> **Institution:** Department of Computer Science & Engineering | B.Tech CSE End-Semester Project Assessment (November 2026)  
> **Project Window:** 16–20 November 2026 (Implementation: 16–18 Nov; PPT Presentations: 19–20 Nov)  
> **Faculty Mentor:** Megha Gupta  
> **Formal PRD:** [docs/PRD_DropOrCop_Group_G.docx](file:///home/antara/Documents/Project/End-sem/docs/PRD_DropOrCop_Group_G.docx) | [DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx](file:///home/antara/Documents/Project/End-sem/DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx)

---

## 👥 Team Members & Responsibilities (Group G)

| Sl. No. | Name | Role & Assigned Ownership |
|:---:|:---|:---|
| **31** | **Harsh Kumar** *(Team Leader)* | **Team Leader & ML Lead:** Clean the dataset, prepare features, and train the single `RandomForestRegressor` model (Phases 1, 2, 3). |
| **32** | **Anamika Ghosh** | **Model Checking Lead:** Create the single train/test split, review held-out predictions, and report selected evaluation results (Phase 4). |
| **34** | **Sinthoiba Kangjam** | **Backend / Integration Lead:** Connect the trained model to the prediction workflow and support integration with the webpage (Phase 5). |
| **35** | **Himesh Vaskar** | **Frontend / UI Lead:** Build the simple webpage form and display estimated resale price, profit/loss, and COP/DROP result (Phase 6). Optional catalog features only if time permits. |

---

## 💡 Overview & Aim

**Overall Aim:** *"The aim of DropOrCop is to make a simple website that uses past sneaker sales to estimate a sneaker’s resale price and possible profit or loss."*

Limited-edition sneaker prices fluctuate dramatically on secondary marketplaces (StockX, GOAT). **DropOrCop** addresses this by:
- Ingesting historical secondary-market transactions (StockX Sneaker Data Contest 2019: Nike x Off-White and Adidas Yeezy releases, 2017–2019).
- Engineering core temporal features (`days_since_release = order_date - release_date`).
- Training a single, robust `RandomForestRegressor` pipeline predicting continuous **Resale Price** ($\hat{P}_{\text{resale}}$).
- Calculating expected net profit or loss downstream:  
  $$\text{Profit / Loss} = \hat{P}_{\text{resale}} - P_{\text{retail}}$$
- Delivering an immediate verdict:
  - 🟢 **COP**: $\text{Estimated Profit} > 0$ (Estimated resale exceeds retail MSRP).
  - 🔴 **DROP**: $\text{Estimated Profit} \le 0$ (Estimated resale at or below retail MSRP).

> **Academic Limitation & Disclaimer:** This estimate is based on historical StockX data from 2017–2019 using four input features (`brand`, `retail_price`, `shoe_size`, `days_since_release`) without sneaker model or colourway granular variables. It is built strictly for student project demonstration, not financial advice or buy/sell recommendations.

---

## 🎯 Measurable Objectives (3-Day Scope)

| ID | Objective | Measurable Success Indicator |
|:---:|:---|:---|
| **O1** | **Data Cleaning** | Ingest historical StockX records, scrub currency characters, calculate `days_since_release`, and remove invalid entries. Output: clean dataset saved to `data/processed/clean_stockx.csv` (94,355 rows, 0 nulls). |
| **O2** | **Single-Model Training** | Prepare selected features and train one `RandomForestRegressor` predicting resale price. Output: exported pipeline artifact `models/best_model.joblib`. |
| **O3** | **Model Checking** | Use one 80/20 train/test split, generate sample predictions on held-out records, and report basic evaluation metrics (`data/processed/test_predictions.csv`). Additional metrics, cross-validation, and diagnostics are optional. |
| **O4** | **Simple Webpage** | Connect trained model to a basic webpage accepting sneaker details and displaying estimated resale price, profit/loss, and COP/DROP verdict. |

---

## 🏗 System Architecture

```text
[StockX Historical Dataset]
             │
             ▼
[Phase 1 & 2: src/data_prep.py] ── Ingestion, cleaning & days_since_release calculation
             │
             ▼
[Phase 3: src/train.py] ────────── Train single RandomForestRegressor -> models/best_model.joblib
             │
             ├───▶ [Phase 4: Evaluation] ── Held-out test predictions (data/processed/test_predictions.csv)
             │
             ▼
[Phase 5: api/main.py] ─────────── FastAPI REST microservice (/predict, /health, /brands)
             │
             ▼
[Phase 6: frontend/] ───────────── Simple web interface with COP / DROP verdict display
```

---

## 📁 Repository Structure

```text
├── api/
│   └── main.py                     # FastAPI REST API service
├── data/
│   ├── raw/                        # Raw StockX transaction dataset
│   └── processed/                  # Cleaned dataset (clean_stockx.csv) & test predictions
├── docs/
│   └── PRD_DropOrCop_Group_G.docx  # Official faculty PRD document
├── frontend/                       # Web interface (React / HTML form)
├── models/
│   └── best_model.joblib           # Trained single RandomForestRegressor pipeline
├── notebooks/                      # Interactive Jupyter exploration & presentation notebooks
│   ├── 01_eda_and_data_cleaning.ipynb
│   └── 02_model_training_and_tuning.ipynb
├── reports/                        # Model comparison & performance reports
├── src/
│   ├── data_prep.py                # Phase 1: Data ingestion and cleansing script
│   ├── train.py                    # Phase 2 & 3: Model training and pipeline serialization
│   └── predict.py                  # Local inference utility
├── DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx  # Latest corrected PRD draft
├── Updated_prd_harshkr.md          # Comprehensive PRD entries & requirements register
├── HARSH_PROJECT_HANDOFF.md        # Technical handoff & phase interface contract
├── task.md                         # Task board tracking core & optional scope
├── progress.md                     # Live progress tracker & milestone metrics
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Data Preparation & Training (Phases 1–3)
```bash
# Clean raw transaction data (FR-01)
python src/data_prep.py

# Train single regression pipeline & export artifact (FR-02, FR-03, FR-04)
python src/train.py
```

### 3. Run FastAPI Backend (Phase 5)
```bash
uvicorn api.main:app --reload --port 8000
```
- Interactive Swagger docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Predict endpoint: `POST http://localhost:8000/predict`

---

## 📄 Documentation Links
- [Updated PRD Reference (Harsh Kumar)](file:///home/antara/Documents/Project/End-sem/Updated_prd_harshkr.md)
- [Task Board](file:///home/antara/Documents/Project/End-sem/task.md)
- [Progress Tracker](file:///home/antara/Documents/Project/End-sem/progress.md)
- [Technical Handoff Contract](file:///home/antara/Documents/Project/End-sem/HARSH_PROJECT_HANDOFF.md)
