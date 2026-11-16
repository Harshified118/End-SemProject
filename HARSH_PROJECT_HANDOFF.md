# 👟 DropOrCop: Machine Learning Pipeline Handoff & Action Plan

> **Instructions for the AI Assistant in a new chat:**  
> Read this document completely. The workspace, virtual environment, GitHub CLI, and MCP integrations are already configured. Resume the project directly from **Current State & Next Immediate Action (Step 1)**.

---

## 📌 1. Project & Role Context

| Field | Detail |
| :--- | :--- |
| **Project Title** | DropOrCop: Sneaker & Streetwear Resale Profit Predictor |
| **Team** | Group G (B.Tech CSE End-Semester Assessment) |
| **Project Window** | 16–18 November 2026 (Implementation) \| 19–20 November (Presentations) |
| **Lead / Owner** | **Harsh Kumar (Sl. No. 31)** — Team Leader & ML Lead |
| **Assigned Scope** | **Phase 1** (Data Ingestion & Cleaning), **Phase 2** (Feature Preprocessing), **Phase 3** (Model Training & Export) |
| **Core Goal** | Train a tabular regression model (`RandomForestRegressor`) predicting resale price on historical StockX data, compute profit/loss, and export the trained model artifact (`models/best_model.joblib`) to unblock downstream teammates. |

### Downstream Team Handoff Register
* **Anamika Ghosh (Sl. No. 32) — Phase 4 (Evaluation Lead):** Needs `data/processed/test_predictions.csv` (`actual_resale_price`, `predicted_resale_price`, `retail_price`, `profit_or_loss`) to run MAE/MAPE/residual diagnostics.
* **Sinthoiba Kangjam (Sl. No. 34) — Phase 5 (API Lead):** Needs `models/best_model.joblib` and the exact JSON payload schema for `/predict`.
* **Himesh Vaskar (Sl. No. 35) — Phase 6 (Frontend Lead):** Needs the prediction response format to build the UI COP/DROP stamp and margin card.

---

## ✅ 2. What Is Already Completed

1. **Project Directory Scaffolding**:
   - `data/raw/` (for raw dataset)
   - `data/processed/` (for cleaned data & test predictions)
   - `src/` (for ML scripts: `data_prep.py`, `train.py`, `predict.py`)
   - `models/` (for serialized pipeline `best_model.joblib`)
   - `notebooks/`, `api/`, `frontend/`, `reports/figures/`
2. **Environment & Dependencies**:
   - Python virtual environment: `venv/` (Python 3.15)
   - [requirements.txt](file:///home/antara/Documents/Project/End-sem/requirements.txt) created with: `pandas`, `numpy`, `scikit-learn`, `joblib`, `matplotlib`, `seaborn`, `openpyxl`, `fastapi`, `uvicorn`.
3. **GitHub Integrations**:
   - **GitHub CLI (`gh`)**: Installed and authenticated as `@Harshified118` (scopes: `repo`, `read:org`, `gist`, `workflow`).
   - **GitHub MCP Server**: Configured globally in `~/.gemini/config/mcp_config.json` via `@modelcontextprotocol/server-github` and verified with live tool calls (`search_repositories`).

---

## 📍 3. Current State & Next Immediate Action

### Step 1: Raw Data Ingestion & Schema Check
* **Dataset**: StockX Sneaker Data Contest (2019) ([Kaggle link](https://www.kaggle.com/datasets/hudsonstuck/stockx-data-contest))
* **Expected Location**: `data/raw/StockX-Data-Contest-2019.csv` (or `.xlsx`)
* **Expected Columns**: `Order Date`, `Brand`, `Sneaker Name`, `Sale Price`, `Retail Price`, `Release Date`, `Shoe Size`, `Buyer Region`
* **Action**: Check if the file is in `data/raw/`. If not, prompt the user or load the available file.

---

## 🛠 4. Sequential Implementation Roadmap

### Phase 1: Data Ingestion & Cleaning (`src/data_prep.py`)
* **Target Script**: `src/data_prep.py`
* **Input**: `data/raw/StockX-Data-Contest-2019.*`
* **Output**: `data/processed/clean_stockx.csv`
* **Transformation Requirements**:
  1. Strip currency symbols (`$`, `,`) and cast `Sale Price` and `Retail Price` to `float64`.
  2. Parse `Order Date` and `Release Date` to datetime.
  3. Calculate elapsed release duration:  
     $$\text{days\_since\_release} = (\text{Order Date} - \text{Release Date}).\text{dt.days}$$
  4. Filter non-physical or corrupted records (`Sale Price > 0`, `days_since_release >= 0`).
  5. Clean column names to snake_case (`order_date`, `brand`, `sneaker_name`, `sale_price`, `retail_price`, `release_date`, `shoe_size`, `buyer_region`, `days_since_release`).
* **Acceptance Condition (FR-01)**: Running `python src/data_prep.py` produces `data/processed/clean_stockx.csv` with 0 nulls in core columns and verified float types.

### Phase 2 & 3: Feature Preprocessing & Model Training (`src/train.py`)
* **Target Script**: `src/train.py`
* **Input**: `data/processed/clean_stockx.csv`
* **Output**:
  - `models/best_model.joblib` (serialized self-contained pipeline)
  - `data/processed/test_predictions.csv` (handoff for Phase 4)
* **Pipeline Architecture**:
  - **Features**: `brand` (Categorical One-Hot / Target encoding), `retail_price`, `shoe_size`, `days_since_release` (StandardScaler).
  - **Target**: `sale_price` (continuous regression).
  - **Estimator**: `RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)`
  - **Downstream Profit Formula**:  
    $$\text{Estimated Profit} = \hat{P}_{\text{sale}} - P_{\text{retail}}$$
* **Acceptance Conditions (FR-02, FR-03, FR-04)**:
  - Model trains in $< 2$ minutes with $R^2 > 0.70$.
  - Pipeline is exported to `models/best_model.joblib` with inference latency $< 50$ ms.
  - `data/processed/test_predictions.csv` contains `[actual_resale_price, predicted_resale_price, retail_price, profit_or_loss]`.

### Phase 4: Team Contract Handoff
1. **To Anamika (Evaluation Lead)**: Provide `data/processed/test_predictions.csv` to calculate MAPE/MAE and generate residual diagnostic plots.
2. **To Sinthoiba (API Lead)**: Provide input schema for `/predict`:
   ```json
   {
     "brand": "Yeezy",
     "retail_price": 220.0,
     "shoe_size": 10.5,
     "days_since_release": 45
   }
   ```
   and response schema:
   ```json
   {
     "estimated_resale_price": 310.50,
     "retail_price": 220.0,
     "estimated_profit": 90.50,
     "profit_margin_pct": 41.14,
     "verdict": "COP"
   }
   ```
3. **To Himesh (Frontend Lead)**: Confirm the `/predict` JSON contract for UI input binding and COP/DROP badge styling.

---

## ⚡ 5. How to Prompt the Agent in the Next Chat

Copy and paste this single prompt into the new conversation window:

```text
Please read HARSH_PROJECT_HANDOFF.md and continue Harsh Kumar's work on DropOrCop. Start by inspecting data/raw/ and executing Phase 1 (src/data_prep.py).
```
