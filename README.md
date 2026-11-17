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

## Work Completed by Phase

### Phases 1–3: ML & Data Pipeline (Harsh Kumar - Sl. No. 31)
- **Data Cleaning (`src/data_prep.py`):** Scrubbed StockX raw transactions, formatted currencies, computed `days_since_release`, exported `data/processed/clean_stockx.csv` (94,355 rows, 0 nulls).
- **Model Training (`src/train.py`):** Trained scikit-learn `RandomForestRegressor` pipeline (One-Hot Encoding + StandardScaler), exported `models/best_model.joblib`.
- **Benchmarking & Handoff:** Algorithm benchmark (`reports/model_comparison_results.csv`), presentation notebooks (`notebooks/`), and holdout predictions (`data/processed/test_predictions.csv`).

### Phase 4: Model Checking & Residual Diagnostics (Anamika Ghosh - Sl. No. 32)
- **Evaluation Script (`src/evaluate.py`):** Independent validation across 18,871 holdout test records.
- **Metric Verification:** Test $R^2$ of `0.6525`, MAE of `$88.69`, RMSE of `$143.71`, MAPE of `20.23%`, and COP/DROP directional accuracy of `99.02%`.
- **Residual Diagnostics & Figures (`reports/figures/`):** Normality histogram, parity scatter plot ($y = x$), homoscedasticity residual plots, and brand error comparison.
- **Reports & Presentation Guide:** Detailed technical report in `reports/evaluation_report.md` and viva cheat sheet in `docs/anamika_presentation_guide.md`.

### Phase 5: Backend REST API & Integration (Sinthoiba Kangjam - Sl. No. 34)
- **FastAPI Service (`api/main.py`):** Model lifecycle management, sub-millisecond inference, Pydantic data validation, and CORS middleware for frontend.
- **Endpoints:** `/` (welcome & meta), `/health` (liveness), `/brands` (catalog metadata), and `POST /predict` (resale valuation & COP/DROP verdict).
- **Automated Tests (`tests/test_api.py`):** 7 unit tests passing with 100% success.
- **Documentation & Presentation Guide:** `docs/API_DOCUMENTATION.md` and `docs/sinthoiba_presentation_guide.md`.

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
