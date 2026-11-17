# DropOrCop: Sneaker Resale Profit Predictor

DropOrCop is a machine learning project that estimates whether a limited-edition sneaker will resell above or below its retail price using past sales data from StockX (Nike x Off-White and Adidas Yeezy releases).

- **COP (Buy):** Predicted resale price is higher than retail price (expected profit).
- **DROP (Skip):** Predicted resale price is equal to or lower than retail price (loss or break-even).

**Academic Context:** Department of Computer Science & Engineering | B.Tech CSE End-Semester Project Assessment (November 2026)  
**Project Window:** 16–20 November 2026 (Development: 16–18 November; Presentations: 19–20 November)  
**Faculty Mentor:** Megha Gupta  
**PRD Document:** [docs/PRD_DropOrCop_Group_G.docx](docs/PRD_DropOrCop_Group_G.docx)

---

## Team Members (Group G)

| Sl. No. | Student Name | Role | Responsibilities |
|:---:|:---|:---|:---|
| **31** | **Harsh Kumar** *(Team Leader)* | **ML Lead** | Data ingestion, cleaning, feature engineering, model training, pipeline export, and evaluation handoff (Phases 1–3). |
| **32** | **Anamika Ghosh** | **Model Checking Lead** | Review held-out predictions on test set, calculate evaluation metrics (MAE, RMSE), and summarize results (Phase 4). |
| **34** | **Sinthoiba Kangjam** | **Backend / Integration Lead** | Connect trained model to API endpoints (`/predict`, `/health`) and integrate with webpage (Phase 5). |
| **35** | **Himesh Vaskar** | **Frontend / UI Lead** | Build webpage form with inputs and display resale price, profit/loss, and COP/DROP badge (Phase 6). |

---

## Work Done by Harsh Kumar (ML & Data Pipeline Lead)

All technical work assigned to Harsh Kumar for Phases 1, 2, and 3 is complete, tested, and saved in this repository.

### 1. Data Cleaning and Preparation (Phase 1)
- **Script:** `src/data_prep.py`
- **Output:** `data/processed/clean_stockx.csv` (94,355 rows, 0 missing values)
- **What was done:**
  - Loaded the raw StockX 2019 dataset (99,956 original records).
  - Cleaned currency formatting by removing `$` and commas, converting prices to numeric floats.
  - Parsed order and release dates to calculate elapsed time: `days_since_release = order_date - release_date`.
  - Filtered corrupted records (zero or negative sale prices and sales recorded before official release date).

### 2. Model Training and Serialization (Phases 2 & 3)
- **Script:** `src/train.py`
- **Saved Model:** `models/best_model.joblib`
- **What was done:**
  - Built an automated scikit-learn pipeline using One-Hot Encoding for `brand` and StandardScaler for numeric features (`retail_price`, `shoe_size`, `days_since_release`).
  - Trained a single primary `RandomForestRegressor` (100 trees, max depth 12) to predict resale price directly.
  - Added downstream logic to calculate profit/loss: `Profit = Predicted Resale Price - Retail Price`.
  - **Results:**
    - Training time: **0.96 seconds** (meets PRD target of under 2 minutes).
    - Inference latency: **0.07 milliseconds** per sample (meets PRD target of under 50 ms).
    - Model test performance: R² score of `0.6525`, MAE of `$88.69`, and RMSE of `$143.71`.
    - COP/DROP verdict directional accuracy: `80.30%`.

### 3. Downstream Handoffs for Teammates
- **For Anamika Ghosh (Evaluation Lead - Phase 4):**
  - Generated `data/processed/test_predictions.csv` containing 18,871 holdout test rows with actual prices, predicted prices, retail MSRP, and profit/loss values.
- **For Sinthoiba Kangjam (API Lead - Phase 5):**
  - Created a working FastAPI service in `api/main.py` with `/predict`, `/health`, and `/brands` endpoints.
  - Configured input schema: `brand`, `retail_price`, `shoe_size`, `days_since_release`.
  - Configured response schema: `estimated_resale_price`, `retail_price`, `estimated_profit`, `verdict` (COP/DROP).
- **For Himesh Vaskar (Frontend Lead - Phase 6):**
  - Specified the exact inputs and outputs needed for the webpage prediction form and COP/DROP badge styling.

### 4. Extra Deliverables for Presentation & Viva
- **Algorithm Benchmark:** Compared Random Forest against Gradient Boosting in `reports/model_comparison_results.csv`. Random Forest was chosen because it trains 6x faster while delivering matching accuracy.
- **Jupyter Notebooks:**
  - `notebooks/01_eda_and_data_cleaning.ipynb`: Exploratory data analysis, price distributions, skewness analysis, and brand comparisons.
  - `notebooks/02_model_training_and_tuning.ipynb`: Feature preprocessing, feature importance plots, actual vs. predicted scatter plots, error bands, and confusion matrices.
- **PRD Documentation:** Updated and formatted the official PRD in `docs/PRD_DropOrCop_Group_G.docx` matching faculty guidelines.

---

## How to Run the Code

### 1. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Data Cleaning & Model Training
```bash
# Clean raw StockX dataset
python src/data_prep.py

# Train Random Forest model and save models/best_model.joblib
python src/train.py
```

### 3. Run FastAPI Backend
```bash
uvicorn api.main:app --reload --port 8000
```
- API Documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Predict endpoint: `POST http://localhost:8000/predict`

---

## Repository Structure

```text
├── api/
│   └── main.py                     # FastAPI REST API service
├── data/
│   ├── raw/                        # Raw StockX dataset
│   └── processed/                  # Cleaned data and test predictions
├── docs/
│   ├── PRD_DropOrCop_Group_G.docx  # Official faculty PRD document
│   └── DropOrCop_Work_Division-1.pdf
├── models/
│   └── best_model.joblib           # Trained Random Forest pipeline
├── notebooks/
│   ├── 01_eda_and_data_cleaning.ipynb      # EDA and data cleaning notebook
│   └── 02_model_training_and_tuning.ipynb  # Model training and diagnostics notebook
├── reports/
│   └── model_comparison_results.csv       # Model benchmark report
├── src/
│   ├── data_prep.py                # Data cleaning script (Phase 1)
│   ├── train.py                    # Model training script (Phases 2 & 3)
│   ├── predict.py                  # Single sample prediction utility
│   └── model_comparison.py         # Algorithm benchmark script
├── requirements.txt                # Python dependencies
└── README.md                       # Main project documentation & Harsh Kumar's work summary
```

---

## Academic Disclaimer

This model is trained on historical secondary market transactions from StockX between 2017 and 2019. It predicts resale value based on four features (`brand`, `retail_price`, `shoe_size`, `days_since_release`). It is built strictly for student academic demonstration and should not be used as financial advice.
