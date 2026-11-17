# DropOrCop: Sneaker Resale Profit Predictor

DropOrCop is a machine-learning web application that estimates whether a limited-edition sneaker will resell above or below its retail price using historical sales data from StockX (Nike x Off-White and Adidas Yeezy releases).

- If the predicted resale price is higher than retail price, the verdict is **COP** (profitable purchase).
- If the predicted resale price is equal to or lower than retail price, the verdict is **DROP** (loss or break-even).

**Academic Context:** Department of Computer Science & Engineering | B.Tech CSE End-Semester Project Assessment (November 2026)  
**Project Window:** 16–20 November 2026 (Development: 16–18 November; Presentations: 19–20 November)  
**Faculty Mentor:** Megha Gupta  
**PRD Document:** [docs/PRD_DropOrCop_Group_G.docx](file:///home/antara/Documents/Project/End-sem/docs/PRD_DropOrCop_Group_G.docx) | [DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx](file:///home/antara/Documents/Project/End-sem/DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx)

---

## Team Members (Group G)

| Sl. No. | Student Name | Role | Responsibilities |
|:---:|:---|:---|:---|
| **31** | **Harsh Kumar** *(Team Leader)* | **ML Lead** | Data ingestion, cleaning, feature engineering, model training, pipeline export, and handoff files (Phases 1–3). |
| **32** | **Anamika Ghosh** | **Model Checking Lead** | Review held-out predictions on test set, calculate evaluation metrics (MAE, RMSE), and summarize results (Phase 4). |
| **34** | **Sinthoiba Kangjam** | **Backend / Integration Lead** | Connect trained model to API endpoints (`/predict`, `/health`) and integrate with webpage (Phase 5). |
| **35** | **Himesh Vaskar** | **Frontend / UI Lead** | Build webpage form with inputs and display resale price, profit/loss, and COP/DROP badge (Phase 6). |

---

## Completed Work from Harsh Kumar's Side (ML & Data Pipeline)

All work assigned to Harsh Kumar (Phases 1, 2, and 3) is **100% complete, tested, and verified on disk**.

### 1. Data Cleaning & Feature Preparation (Phase 1)
- **Script:** [src/data_prep.py](file:///home/antara/Documents/Project/End-sem/src/data_prep.py)
- **Output:** [data/processed/clean_stockx.csv](file:///home/antara/Documents/Project/End-sem/data/processed/clean_stockx.csv) (94,355 rows, 0 nulls)
- **What was done:**
  - Loaded raw StockX 2019 dataset (99,956 original records).
  - Cleaned currency formatting (`$` and commas) and converted prices to numerical floats.
  - Parsed order and release dates to compute the key feature: `days_since_release = order_date - release_date`.
  - Removed corrupted records (non-positive sale prices and sales recorded before official release date).

### 2. Model Training & Serialization (Phases 2 & 3)
- **Script:** [src/train.py](file:///home/antara/Documents/Project/End-sem/src/train.py)
- **Model Artifact:** [models/best_model.joblib](file:///home/antara/Documents/Project/End-sem/models/best_model.joblib)
- **What was done:**
  - Built an automated scikit-learn pipeline using One-Hot Encoding for `brand` and StandardScaler for `retail_price`, `shoe_size`, and `days_since_release`.
  - Trained a single primary `RandomForestRegressor` (100 trees, max depth 12) to predict resale price directly.
  - Calculated downstream profit or loss: `Profit = Predicted Resale Price - Retail Price`.
  - **Performance results:**
    - Training time: **0.96 seconds** (well within the PRD target of under 2 minutes).
    - Inference latency: **0.07 milliseconds** per shoe (well within the PRD target of under 50 ms).
    - Holdout test R²: `0.6525`, MAE: `$88.69`, RMSE: `$143.71`.
    - Directional COP/DROP accuracy: `80.30%`.

### 3. Handoff Files Provided for Downstream Teammates
- **For Anamika Ghosh (Phase 4 - Evaluation):**
  - Generated [data/processed/test_predictions.csv](file:///home/antara/Documents/Project/End-sem/data/processed/test_predictions.csv) containing 18,871 holdout test rows with actual resale prices, predicted prices, retail prices, and profit/loss values.
- **For Sinthoiba Kangjam (Phase 5 - API Backend):**
  - Built and verified [api/main.py](file:///home/antara/Documents/Project/End-sem/api/main.py) with `/predict`, `/health`, and `/brands` endpoints using FastAPI.
  - Documented exact request and response JSON schemas in [HARSH_PROJECT_HANDOFF.md](file:///home/antara/Documents/Project/End-sem/HARSH_PROJECT_HANDOFF.md).
- **For Himesh Vaskar (Phase 6 - Frontend UI):**
  - Verified input fields needed (`brand`, `retail_price`, `shoe_size`, `days_since_release`) and output display logic for estimated price, profit/loss, and COP/DROP badge.

### 4. Extra Deliverables Completed for Final Presentation
- **Model Benchmark:** Benchmarked Random Forest against Gradient Boosting in [reports/model_comparison_results.csv](file:///home/antara/Documents/Project/End-sem/reports/model_comparison_results.csv). Random Forest was selected because it trains 6x faster while delivering matching accuracy.
- **Presentation Notebooks:**
  - [notebooks/01_eda_and_data_cleaning.ipynb](file:///home/antara/Documents/Project/End-sem/notebooks/01_eda_and_data_cleaning.ipynb): Data distributions, skewness analysis, brand ROI comparisons (Yeezy vs. Off-White), and release date trends.
  - [notebooks/02_model_training_and_tuning.ipynb](file:///home/antara/Documents/Project/End-sem/notebooks/02_model_training_and_tuning.ipynb): Feature importances, actual vs. predicted scatter plots, error bands, and confusion matrices ready for PPT presentation slides.
- **PRD Synchronization:** Formatted and synced the revised PRD across [docs/PRD_DropOrCop_Group_G.docx](file:///home/antara/Documents/Project/End-sem/docs/PRD_DropOrCop_Group_G.docx) and [Updated_prd_harshkr.md](file:///home/antara/Documents/Project/End-sem/Updated_prd_harshkr.md).

---

## How to Run the Project

### 1. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Data Cleaning & Model Training
```bash
# Clean raw StockX dataset (creates data/processed/clean_stockx.csv)
python src/data_prep.py

# Train Random Forest pipeline and export models/best_model.joblib
python src/train.py
```

### 3. Run FastAPI Backend Server
```bash
uvicorn api.main:app --reload --port 8000
```
- Interactive API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`
- Predict Endpoint: `POST http://localhost:8000/predict`

---

## Repository Structure

```text
├── api/
│   └── main.py                     # FastAPI REST API service
├── data/
│   ├── raw/                        # Raw StockX dataset
│   └── processed/                  # Cleaned data (clean_stockx.csv) and test predictions
├── docs/
│   └── PRD_DropOrCop_Group_G.docx  # Official faculty PRD document
├── frontend/                       # Web interface (prediction form)
├── models/
│   └── best_model.joblib           # Trained single Random Forest model pipeline
├── notebooks/
│   ├── 01_eda_and_data_cleaning.ipynb      # EDA and data cleaning visual notebook
│   └── 02_model_training_and_tuning.ipynb  # Model training and diagnostics notebook
├── reports/
│   └── model_comparison_results.csv       # Model benchmark results
├── src/
│   ├── data_prep.py                # Data cleaning script (Phase 1)
│   ├── train.py                    # Model training script (Phases 2 & 3)
│   ├── predict.py                  # Single sample prediction utility
│   └── model_comparison.py         # Algorithm benchmark script
├── DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx  # Faculty PRD draft
├── Updated_prd_harshkr.md          # Comprehensive PRD entries & requirement tracking
├── HARSH_PROJECT_HANDOFF.md        # Technical handoff details for teammates
├── task.md                         # Task board tracking all phases
├── progress.md                     # Live progress and metrics tracker
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## Limitations & Disclaimer

This model is trained on historical secondary market transactions from StockX between 2017 and 2019. It predicts resale value based on four features (`brand`, `retail_price`, `shoe_size`, `days_since_release`) without taking specific colorways or current market hype into account. This project is built strictly for student academic demonstration and should not be used as financial advice.
