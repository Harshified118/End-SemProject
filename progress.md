# 📈 DropOrCop: Live Progress Tracker

> Updated continuously as milestones are completed.  
> **Group:** Group G | **Faculty Mentor:** Megha Gupta  
> **Project Window:** 16–20 November 2026 (Implementation: 16–18 Nov; PPT: 19–20 Nov)  
> **PRD Source:** [docs/PRD_DropOrCop_Group_G.docx](file:///home/antara/Documents/Project/End-sem/docs/PRD_DropOrCop_Group_G.docx) / [DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx](file:///home/antara/Documents/Project/End-sem/DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx)

---

## 🟢 Overall Project Status: **ON TRACK**

| Phase | Description | Scope Level | Owner | Status | Completion Date |
|:---:|:---|:---:|:---|:---:|:---:|
| **1** | Data Ingestion, Cleaning & `days_since_release` (FR-01) | **Core** | Harsh Kumar (Sl. No. 31) | **Completed** | 16-Nov-2026 |
| **2 & 3** | Single-Model Training (`RandomForestRegressor`) & Serialization (FR-02, FR-03) | **Core** | Harsh Kumar (Sl. No. 31) | **Completed** | 16-Nov-2026 |
| **4** | Model Checking & Sample Evaluation Handoff (FR-04, FR-12) | **Core** | Anamika Ghosh (Sl. No. 32) | **Completed** *(Held-out test set generated; sample review in progress)* | 16-Nov-2026 |
| **5** | FastAPI Backend Prediction Service (FR-05) | **Core** | Sinthoiba Kangjam (Sl. No. 34) | **Completed** | 16-Nov-2026 |
| **6** | Simple Webpage UI with COP/DROP Display (FR-06, FR-11) | **Core** | Himesh Vaskar (Sl. No. 35) | *In Progress* | Pending |
| **Extras**| Model Benchmark & Presentation Notebooks (FR-12, FR-13) | *Optional* | Harsh Kumar (Sl. No. 31) | **Completed** | 16-Nov-2026 |
| **7** | Final Documentation, PRD & Presentation Deck | **Core** | Group G (All 4 Members) | *In Progress* | 19-Nov-2026 |

---

## 🏆 Completed Milestones & Metrics

### 1. Data Cleaning (`data/processed/clean_stockx.csv`)
* **Input Records:** 99,956 raw transactions from StockX 2019 dataset.
* **Filtered Records:** 5,601 corrupt/negative rows removed (`sale_price <= 0` or `days_since_release < 0`).
* **Output Records:** **94,355 rows**, 0 missing values across core features.
* **Engineered Feature:** $\text{days\_since\_release} = (\text{Order Date} - \text{Release Date})$.

### 2. Model Training & Pipeline (`models/best_model.joblib`)
* **Algorithm:** Single `RandomForestRegressor(n_estimators=100, max_depth=12, min_samples_leaf=5, random_state=42)`
* **Train Time:** **0.96 seconds** (meets PRD target $< 120$ s — **PASSED**)
* **Inference Latency:** **0.07 ms** per sample (meets PRD target $< 50$ ms — **PASSED**)
* **Model Test Performance ($N = 18,871$ holdout test samples):**
  * **$R^2$ Score:** `0.6525`
  * **MAE:** `$88.69`
  * **MAPE:** `20.23%`
  * **RMSE:** `$143.71`
  * **COP / DROP Verdict Accuracy:** `80.30%` (F1-score: 0.89 on COP)

### 3. Optional Model Benchmark (`reports/model_comparison_results.csv`)
* **RandomForest vs. GradientBoosting:**
  * Both achieve comparable accuracy ($R^2 \approx 0.6525$ vs $0.6543$, MAE $\$88.69$ vs $\$89.22$).
  * **RandomForest is 6× faster to train** (0.96s vs 5.99s) with parallel multi-core scaling.
  * Selected **RandomForestRegressor** as the primary champion pipeline per PRD O2.

### 4. Interactive Jupyter Notebooks (`notebooks/`) — Fully Executed & Visualized
* **[notebooks/01_eda_and_data_cleaning.ipynb](file:///home/antara/Documents/Project/End-sem/notebooks/01_eda_and_data_cleaning.ipynb):**
  * Visual audit and non-null verification.
  * Price distributions showing extreme right-skewness ($\text{skew} = 3.65$, max resale $\$4,050$).
  * Brand breakdown: Yeezy high liquidity (74.1% volume, 43% median ROI) vs. Off-White scarcity premium (275% median ROI).
  * Impact of `days_since_release`: Binned analysis showing Yeezy delivery dip (15–45d) vs. continuous Off-White deadstock appreciation.
* **[notebooks/02_model_training_and_tuning.ipynb](file:///home/antara/Documents/Project/End-sem/notebooks/02_model_training_and_tuning.ipynb):**
  * Preprocessing visualizations: `StandardScaler` distribution comparisons & correlation heatmap.
  * Feature importance ranking: Retail Price & Brand dominate (~72%), Days Since Release (~19%), Shoe Size (~9%).
  * Actual vs. Predicted resale price scatter plot with 45° identity line, $\pm 20\%$ error band, and COP/DROP confusion matrix.
  * Side-by-side performance comparison against `GradientBoostingRegressor`.
  * Live mock inference verification with sample JSON payloads matching the FastAPI schema.

### 5. Downstream Team Handoffs Ready
* **Phase 4 Handoff (Anamika Ghosh - Model Checking):** [data/processed/test_predictions.csv](file:///home/antara/Documents/Project/End-sem/data/processed/test_predictions.csv) (18,871 holdout test predictions with actuals, predicted prices, retail MSRP, and profit/loss).
* **Phase 5 Handoff (Sinthoiba Kangjam - Backend/API):** [models/best_model.joblib](file:///home/antara/Documents/Project/End-sem/models/best_model.joblib) & [api/main.py](file:///home/antara/Documents/Project/End-sem/api/main.py) with `/predict`, `/health`, and `/brands`.
* **PRD Document Alignment:** Synchronized [docs/PRD_DropOrCop_Group_G.docx](file:///home/antara/Documents/Project/End-sem/docs/PRD_DropOrCop_Group_G.docx) and [DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx](file:///home/antara/Documents/Project/End-sem/DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx) incorporating faculty feedback (Faculty Mentor: Megha Gupta, 4 team members).

---

## ⏭️ Immediate Next Steps

1. **Frontend UI (`frontend/`)**:
   - Complete simple webpage with interactive input fields (Brand dropdown, Retail Price, Shoe Size, Days Since Release) and COP/DROP badge display connecting to `POST /predict` (FR-06).
   - Ensure responsive layout without horizontal scrolling (FR-11).
2. **Slide Deck & Viva Defense Prep**:
   - Synthesize plots and benchmark tables from `notebooks/` into PPT slides for 19–20 November reviews.
