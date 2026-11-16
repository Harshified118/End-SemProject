# 📈 DropOrCop: Live Progress Tracker

> Updated continuously as milestones are completed.

---

## 🟢 Overall Project Status: **ON TRACK**

| Phase | Description | Owner | Status | Completion Date |
|:---:|:---|:---|:---:|:---:|
| **1** | Data Cleaning & Feature Engineering | Harsh Kumar | **Completed** | 16-Nov-2026 |
| **2 & 3** | Model Training, Tuning & Export | Harsh Kumar | **Completed** | 16-Nov-2026 |
| **4** | Model Evaluation & Residual Diagnostics | Anamika Ghosh | *Ready for Handoff* | Pending |
| **5** | FastAPI Backend Service | Sinthoiba Kangjam | **Completed** | 16-Nov-2026 |
| **6** | Frontend UI & COP/DROP Display | Himesh Vaskar | *In Progress* | Pending |
| **7** | Slides, Notebooks & Presentation | Group G | *In Progress* | 19-Nov-2026 |

---

## 🏆 Completed Milestones & Metrics

### 1. Data Cleaning (`data/processed/clean_stockx.csv`)
* **Input Records:** 99,956 raw transactions.
* **Filtered Records:** 5,601 corrupt/negative rows removed.
* **Output Records:** **94,355 rows**, 0 missing values across core features.
* **Engineered Feature:** `days_since_release = (order_date - release_date).dt.days`.

### 2. Model Training & Pipeline (`models/best_model.joblib`)
* **Algorithm:** `RandomForestRegressor(n_estimators=100, max_depth=12, min_samples_leaf=5, random_state=42)`
* **Train Time:** **0.98 seconds** (target $< 120$ s — **PASSED**)
* **Single Inference Latency:** **43.72 ms** (target $< 50$ ms — **PASSED**)
* **Model Test Performance:**
  * **$R^2$ Score:** `0.6525`
  * **MAE:** `$88.69`
  * **MAPE:** `20.23%`
  * **RMSE:** `$143.71`

### 3. Downstream Handoffs Ready
* **Phase 4 Handoff (Anamika):** [data/processed/test_predictions.csv](file:///home/antara/Documents/Project/End-sem/data/processed/test_predictions.csv) (18,871 test samples with actual vs. predicted prices).
* **Phase 5 Handoff (Sinthoiba):** [api/main.py](file:///home/antara/Documents/Project/End-sem/api/main.py) with `/predict`, `/health`, and `/brands`.
* **Database MCP Setup:** SQLite initialized at [data/droporcop.db](file:///home/antara/Documents/Project/End-sem/data/droporcop.db).

---

## ⏭️ Immediate Next Steps

1. **Jupyter Notebooks for Faculty Presentation (`notebooks/`)**:
   - Create `01_eda.ipynb` (data distributions, Yeezy vs. Off-White comparison).
   - Create `02_model_training.ipynb` (model evaluation, actual vs predicted scatter plots).
2. **Frontend UI (`frontend/`)**:
   - Build a lightweight `index.html` with COP/DROP stamp and API fetch call.
3. **Evaluation Plots (`reports/figures/`)**:
   - Generate residual plots for Anamika to include in the final report.
