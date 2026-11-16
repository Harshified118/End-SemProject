# 📋 DropOrCop: Project Task Board

> Tracks tasks across all project phases for Group G (Assessment Window: 16–20 November 2026).

---

## 👟 Phase 1: Data Ingestion & Cleaning
**Owner:** Harsh Kumar (Sl. No. 31) — *ML Lead*
- [x] Ingest raw StockX 2019 dataset (`data/raw/StockX-Data-Contest-2019-3.csv`).
- [x] Scrub currency strings (`$`, `,`) and convert prices to `float64`.
- [x] Parse `order_date` and `release_date` to datetime.
- [x] Feature engineering: compute elapsed time `days_since_release`.
- [x] Filter invalid records (`sale_price > 0`, `days_since_release >= 0`).
- [x] Export cleaned dataset to `data/processed/clean_stockx.csv` (94,355 rows, 0 nulls).

---

## 🤖 Phase 2 & 3: Model Training & Serialization
**Owner:** Harsh Kumar (Sl. No. 31) — *ML Lead*
- [x] Preprocessing pipeline: `OneHotEncoder` for `brand`, `StandardScaler` for numeric inputs.
- [x] Train baseline `RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)`.
- [x] Verify training time ($< 2$ minutes) and inference latency ($< 50$ ms).
- [x] Serialize model pipeline to `models/best_model.joblib`.
- [x] Generate downstream test predictions file `data/processed/test_predictions.csv`.
- [x] Benchmark against `GradientBoostingRegressor` (`reports/model_comparison_results.csv`).
- [ ] Create Jupyter presentation notebooks in `notebooks/` (`01_eda.ipynb`, `02_model_training.ipynb`).

---

## 📊 Phase 4: Model Evaluation & Diagnostics
**Owner:** Anamika Ghosh (Sl. No. 32) — *Evaluation Lead*
- [ ] Load `data/processed/test_predictions.csv`.
- [ ] Compute evaluation metrics: MAE, MAPE, RMSE, $R^2$.
- [ ] Generate residual scatter plots and distribution histogram (`reports/figures/`).
- [ ] Identify and document top-5 outlier predictions.

---

## ⚡ Phase 5: API & Backend Service
**Owner:** Sinthoiba Kangjam (Sl. No. 34) — *API Lead*
- [x] Implement FastAPI service in `api/main.py`.
- [x] Endpoint `POST /predict`: Input `brand`, `retail_price`, `shoe_size`, `days_since_release`.
- [x] Endpoint `GET /health` and `GET /brands`.
- [ ] Test API integration and verify latency with load testing.

---

## 🎨 Phase 6: Frontend & UI
**Owner:** Himesh Vaskar (Sl. No. 35) — *Frontend Lead*
- [ ] Create `frontend/index.html` with clean dark sneaker-marketplace theme.
- [ ] Build input controls (brand dropdown, retail price, shoe size, days slider).
- [ ] Add animated COP (green) / DROP (red) verdict stamp.
- [ ] Connect frontend `fetch()` to `POST http://localhost:8000/predict`.

---

## 📑 Phase 7: Final Documentation & Presentation
**Owner:** Entire Team (Group G)
- [x] Concise `README.md` with team roles and setup instructions.
- [x] Maintain `task.md` and `progress.md`.
- [ ] Prepare slide deck (PPT) for presentation (19–20 November).
