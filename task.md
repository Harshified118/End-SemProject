# 📋 DropOrCop: Project Task Board

> Tracks tasks across all project phases for Group G per the revised PRD (`DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx`).  
> **Project Window:** 16–20 November 2026 (Implementation: 16–18 Nov; PPT Presentations: 19–20 Nov)  
> **Faculty Mentor:** Megha Gupta  

---

## 👥 Team Roster & Ownership
* **Harsh Kumar (Sl. No. 31)** — *Team Leader & ML Lead:* Clean the dataset, prepare features, and train the single `RandomForestRegressor` model (Phases 1, 2, 3).
* **Anamika Ghosh (Sl. No. 32)** — *Model Checking Lead:* Create the single train/test split, review held-out predictions, and report selected evaluation results (Phase 4).
* **Sinthoiba Kangjam (Sl. No. 34)** — *Backend / Integration Lead:* Connect the trained model to the prediction workflow and support integration with the webpage (Phase 5).
* **Himesh Vaskar (Sl. No. 35)** — *Frontend / UI Lead:* Build the simple webpage form and display estimated resale price, profit/loss, and COP/DROP result (Phase 6). Optional catalog features only if time permits.

---

## 👟 Phase 1: Data Ingestion & Cleaning (Core Scope)
**Owner:** Harsh Kumar (Sl. No. 31) | **Requirement:** FR-01 (Must) | **Objective:** O1
- [x] Ingest raw StockX 2019 dataset (`data/raw/StockX-Data-Contest-2019-3.csv`).
- [x] Scrub currency strings (`$`, `,`) and convert prices to `float64`.
- [x] Parse `order_date` and `release_date` to standard datetimes.
- [x] Calculate elapsed release duration: $\text{days\_since\_release} = (\text{Order Date} - \text{Release Date})$.
- [x] Filter non-physical records (`sale_price > 0`, `days_since_release >= 0`).
- [x] Export cleaned dataset to `data/processed/clean_stockx.csv` (94,355 rows, 0 nulls).

---

## 🤖 Phases 2 & 3: Feature Preprocessing & Single-Model Pipeline (Core Scope)
**Owner:** Harsh Kumar (Sl. No. 31) | **Requirements:** FR-02, FR-03, FR-04 (Must) | **Objective:** O2
- [x] Preprocessing pipeline: `OneHotEncoder` for `brand`, `StandardScaler` for continuous inputs (`retail_price`, `shoe_size`, `days_since_release`).
- [x] Train single primary `RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)` predicting continuous resale price directly.
- [x] Verify training time ($< 2$ minutes target) and inference latency ($< 50$ ms target).
- [x] Serialize model pipeline to `models/best_model.joblib` (FR-03).
- [x] Export holdout test set predictions table to `data/processed/test_predictions.csv` for Phase 4 handoff (FR-04).
- [x] Compute downstream profit/loss: $\text{Profit} = \hat{P}_{\text{resale}} - P_{\text{retail}}$ and COP/DROP verdict.

### 🌟 Phases 2 & 3: Optional Enhancements (Completed)
**Requirements:** FR-12, FR-13 (Could-have)
- [x] Benchmark against secondary algorithm (`GradientBoostingRegressor`) in `reports/model_comparison_results.csv` (FR-13).
- [x] Interactive Jupyter presentation notebooks created in `notebooks/`:
  - `notebooks/01_eda_and_data_cleaning.ipynb`
  - `notebooks/02_model_training_and_tuning.ipynb`

---

## 📊 Phase 4: Model Checking & Evaluation
**Owner:** Anamika Ghosh (Sl. No. 32) | **Requirements:** FR-04, FR-12 | **Objective:** O3
### Core Tasks (Essential 3-Day Scope)
- [x] Set up single 80/20 train/test split with fixed random seed (`random_state=42`).
- [x] Generate test set predictions on held-out records (`data/processed/test_predictions.csv`).
- [ ] Review sample held-out predictions and record basic evaluation summary (MAE, RMSE).

### Optional Evaluation Checks (Could-have)
- [x] Extended metrics calculated: MAE ($88.69), RMSE ($143.71), MAPE (20.23%), $R^2$ (0.6525), Verdict Accuracy (80.30%).
- [x] Residual diagnostic visualizations and error band analysis (documented in notebook `02`).
- [ ] Document top-5 outlier predictions for viva defense presentation.

---

## ⚡ Phase 5: Backend / API Integration
**Owner:** Sinthoiba Kangjam (Sl. No. 34) | **Requirement:** FR-05 (Must)
- [x] Build FastAPI service in `api/main.py`.
- [x] Route `POST /predict`: accepts `brand`, `retail_price`, `shoe_size`, `days_since_release` and returns `estimated_resale_price`, `retail_price`, `estimated_profit_or_loss`, `verdict` (COP/DROP).
- [x] Routes `GET /health` and `GET /brands`.
- [x] Pydantic input validation & error handling for invalid/missing values.
- [ ] Verify frontend-to-backend integration and response latency ($< 100$ ms target).

---

## 🎨 Phase 6: Frontend & UI
**Owner:** Himesh Vaskar (Sl. No. 35) | **Requirements:** FR-06, FR-11 (Must), FR-07 to FR-10 (Could-have) | **Objective:** O4
### Core Webpage (Essential 3-Day Scope)
- [ ] Build simple prediction form with input controls: `brand` dropdown, `retail_price`, `shoe_size`, `days_since_release` slider/input (FR-06).
- [ ] Display output results: Estimated Resale Price, Estimated Profit/Loss, and COP/DROP badge (FR-06).
- [ ] Graceful fallback error banners for network or input validation issues without crashing (NFR Reliability).
- [ ] Responsive design across desktop, tablet, and mobile (FR-11).

### Optional Extras (Only If Time Permits — May Be Omitted per PRD)
- [ ] FR-07: Illustrative sneaker catalog display.
- [ ] FR-08: Catalog search filter.
- [ ] FR-09: Session save/unsave state toggle.
- [ ] FR-10: Product detail preview modal.

---

## 📑 Phase 7: Documentation, PRD & Presentation
**Owner:** Entire Team (Group G)
- [x] Synchronize PRD Word document: [docs/PRD_DropOrCop_Group_G.docx](file:///home/antara/Documents/Project/End-sem/docs/PRD_DropOrCop_Group_G.docx) / [DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx](file:///home/antara/Documents/Project/End-sem/DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx).
- [x] Maintain team registers, PRD entries, and technical handoffs in [Updated_prd_harshkr.md](file:///home/antara/Documents/Project/End-sem/Updated_prd_harshkr.md) and [HARSH_PROJECT_HANDOFF.md](file:///home/antara/Documents/Project/End-sem/HARSH_PROJECT_HANDOFF.md).
- [x] Maintain [README.md](file:///home/antara/Documents/Project/End-sem/README.md), [task.md](file:///home/antara/Documents/Project/End-sem/task.md), and [progress.md](file:///home/antara/Documents/Project/End-sem/progress.md).
- [ ] Prepare final presentation slide deck (PPT) for 19–20 November reviews.
