# 👟 DropOrCop: Machine Learning Pipeline Handoff & Action Plan

> **Instructions for the AI Assistant in a new chat:**  
> Read this document completely. The workspace, virtual environment, and core ML pipeline are already implemented and aligned with the revised PRD (`DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx` / `docs/PRD_DropOrCop_Group_G.docx`).

---

## 📌 1. Project & Role Context

| Field | Detail |
| :--- | :--- |
| **Project Title** | DropOrCop: Sneaker & Streetwear Resale Profit Predictor |
| **Team** | Group G (B.Tech CSE End-Semester Assessment, November 2026) |
| **Project Window** | 16–20 November 2026 (Implementation: 16–18 Nov; Presentations: 19–20 Nov) |
| **Faculty Mentor** | Megha Gupta |
| **Lead / Owner** | **Harsh Kumar (Sl. No. 31)** — Team Leader & ML Lead |
| **Assigned Scope** | Clean the dataset, prepare features and train the single `RandomForestRegressor` model (Phases 1, 2, 3) |
| **Core Goal** | Ingest & clean historical StockX records, engineer `days_since_release`, train a single robust `RandomForestRegressor` predicting resale price directly, calculate downstream profit/loss, and export the trained artifact (`models/best_model.joblib`) along with holdout test predictions (`data/processed/test_predictions.csv`). |

### Confirmed Team Register (4 Members)
* **Harsh Kumar (Sl. No. 31) — Team Leader & ML Lead:** Clean the dataset, prepare features, and train the single `RandomForestRegressor` model (Phases 1, 2, 3).
* **Anamika Ghosh (Sl. No. 32) — Model Checking Lead (Phase 4):** Create the single train/test split, review held-out predictions (`data/processed/test_predictions.csv`), and report basic evaluation results.
* **Sinthoiba Kangjam (Sl. No. 34) — Backend / Integration Lead (Phase 5):** Connect the trained model (`models/best_model.joblib`) to the prediction workflow (`api/main.py`) and support webpage integration.
* **Himesh Vaskar (Sl. No. 35) — Frontend / UI Lead (Phase 6):** Build the simple webpage form and display estimated resale price, profit/loss, and COP/DROP result. Optional catalog features only if time permits.

---

## ✅ 2. What Is Already Completed

1. **Phase 1: Data Ingestion & Cleaning (`src/data_prep.py` - FR-01, O1)**:
   - Ingested 99,956 raw records from `data/raw/StockX-Data-Contest-2019-3.csv`.
   - Stripped currency symbols (`$`, `,`) and cast prices to `float64`.
   - Calculated $\text{days\_since\_release} = (\text{Order Date} - \text{Release Date})$.
   - Filtered corrupted records (`sale_price <= 0`, `days_since_release < 0`).
   - Saved 94,355 clean records to `data/processed/clean_stockx.csv` (0 nulls).
2. **Phases 2 & 3: Model Training & Pipeline Serialization (`src/train.py` - FR-02, FR-03, FR-04, O2)**:
   - Built encapsulated pipeline: `OneHotEncoder` for `brand`, `StandardScaler` for numeric inputs.
   - Trained single primary `RandomForestRegressor(n_estimators=100, max_depth=12, min_samples_leaf=5, random_state=42)`.
   - Verified training time (0.96s vs $< 120$s target) and inference latency (0.07ms vs $< 50$ms target).
   - Exported self-contained artifact to `models/best_model.joblib`.
   - Exported 18,871 holdout test predictions to `data/processed/test_predictions.csv`.
3. **Optional Enhancements (FR-12, FR-13)**:
   - Benchmarked against `GradientBoostingRegressor` (`reports/model_comparison_results.csv`).
   - Fully executed presentation notebooks:
     - `notebooks/01_eda_and_data_cleaning.ipynb`
     - `notebooks/02_model_training_and_tuning.ipynb`
4. **Phase 5: Backend REST API (`api/main.py` - FR-05)**:
   - FastAPI microservice with endpoints `POST /predict`, `GET /health`, `GET /brands`.
5. **PRD & Documentation Alignment**:
   - Synchronized Word PRD: `docs/PRD_DropOrCop_Group_G.docx` & `DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx`.
   - Updated `Updated_prd_harshkr.md`, `README.md`, `task.md`, and `progress.md`.

---

## 🛠 3. Downstream Team Interface Contracts

### 1. To Anamika Ghosh (Model Checking Lead - Phase 4)
* **File provided:** `data/processed/test_predictions.csv`
* **Contents:** 18,871 test samples with columns `[actual_resale_price, predicted_resale_price, retail_price, profit_or_loss, days_since_release, brand, shoe_size]`.
* **Action:** Review sample predictions and record basic evaluation summary (MAE: \$88.69, RMSE: \$143.71, $R^2$: 0.6525).

### 2. To Sinthoiba Kangjam (Backend / Integration Lead - Phase 5)
* **Model artifact provided:** `models/best_model.joblib`
* **Input Schema (`POST /predict`):**
  ```json
  {
    "brand": "Yeezy",
    "retail_price": 220.0,
    "shoe_size": 10.5,
    "days_since_release": 45
  }
  ```
* **Response Schema:**
  ```json
  {
    "estimated_resale_price": 310.50,
    "retail_price": 220.0,
    "estimated_profit": 90.50,
    "profit_margin_pct": 41.14,
    "verdict": "COP"
  }
  ```

### 3. To Himesh Vaskar (Frontend / UI Lead - Phase 6)
* **Webpage requirements (FR-06, FR-11):** Simple prediction form with Brand dropdown, Retail MSRP, Shoe Size, Days Since Release, and visible displays for Estimated Resale Price, Estimated Profit/Loss, and COP/DROP badge. Optional catalog features may be omitted per PRD scope.

---

## ⚡ 4. Next Immediate Actions
1. Support Himesh Vaskar with frontend connection to `POST http://localhost:8000/predict`.
2. Prepare presentation slide deck (PPT) for 19–20 November reviews using metrics and charts from `notebooks/`.
