# PRD Section Entries: Harsh Kumar (Sl. No. 31) [REVISED]
**Project Title:** DropOrCop: Sneaker & Streetwear Resale Profit Predictor  
**Group:** Group G  
**Assigned Ownership:** Phase 1 (Data Ingestion & Cleaning), Phase 2 (Feature Preprocessing), Phase 3 (Model Training & Export)  
**Revision Date:** 16-11-2026 (Revised per Faculty Reviewer Feedback)  
**Target Document:** `PRD_DropOrCop_Group_G.docx`

---

## 📌 Document & Team Details

| PRD Field | Entry to Fill |
| :--- | :--- |
| **Group ID** | Group G |
| **Assigned Project Title** | DropOrCop: Sneaker & Streetwear Resale Profit Predictor |
| **Programme / Course / Semester** | B.Tech in Computer Science & Engineering / End-Semester Project Assessment |
| **Project Window** | 16–20 November 2026 (Project work: 16–18 November; PPT presentations: 19–20 November) |
| **Team Leader / Coordinator** | Harsh Kumar (Sl. No. 31) |
| **PRD Submission Date** | 16-11-2026 (Resubmission Draft) |

### Team Member Register (Table 2)
| No. | Student Name | Contact / Role Description |
| :--- | :--- | :--- |
| **1** | **Harsh Kumar** (Sl. No. 31) | **Team Leader & ML Lead:** Data Ingestion, Feature Preprocessing & Single-Model Pipeline (Phases 1, 2, 3) |
| 2 | Anamika Ghosh (Sl. No. 32) | Evaluation Lead: Test set evaluation (MAPE/MAE) & sample verification checks (Phase 4) |
| 3 | [Student Name - Sl. No. 33] | Data Support & Testing: Exploratory data analysis assistance & integration testing |
| 4 | Sinthoiba Kangjam (Sl. No. 34) | API & Backend Lead: Lightweight FastAPI service (`/predict`, `/health`) (Phase 5) |
| 5 | Himesh Vaskar (Sl. No. 35) | Frontend Lead: Simple web interface with input fields & prediction display (Phase 6) |

---

## 📌 1. Project Summary (Data & ML Pipeline Perspective)
*Copy-paste into PRD Section 1 Table:*

> DropOrCop is a machine-learning web application that uses historical sneaker transaction data to estimate a sneaker's resale price and determine its potential profit or loss against retail cost. Using historical secondary market transaction records from StockX (covering Nike x Off-White and Adidas Yeezy releases), the pipeline cleans price string formatting, calculates the elapsed release duration (`days_since_release`), and encodes core sneaker attributes (`brand`, `shoe_size`, `retail_price`). A single, robust `RandomForestRegressor` ensemble is trained to predict the estimated resale price. From this prediction, estimated net profit or loss is calculated as $(\text{Estimated Resale Price} - \text{Retail Price})$. The trained model is serialized into `models/best_model.joblib` for zero-latency inference via a lightweight FastAPI backend and presented through a clean web interface. Advanced comparative modeling (e.g., Gradient Boosting) and extensive hyperparameter grid searching are retained as optional enhancements.

---

## 📌 2. Background and Problem Statement
*Copy-paste into PRD Section 2 Table:*

> Limited-edition sneakers frequently trade on secondary marketplaces at prices significantly higher or lower than their original retail prices. Buyers and casual collectors often struggle to gauge whether an upcoming drop will appreciate or depreciate, risking financial loss when paying retail for drops that drop below retail price. DropOrCop addresses this problem by training a regression model on historical secondary market transactions to estimate future resale values and provide an immediate, data-backed profit or loss forecast prior to purchase.

---

## 📌 3. Aim, Objectives and Success Indicators
*Copy-paste into PRD Section 3 Table:*

**Overall Aim:**  
> **"The aim of DropOrCop is to make a simple website that uses past sneaker sales to estimate a sneaker’s resale price and possible profit or loss."**

### Measurable Objectives for 3-Day Implementation (16–18 November)
| Objective ID | Objective Description | Measurable Success Indicator |
| :--- | :--- | :--- |
| **O1** | **Data Ingestion & Cleaning (Phase 1):** Ingest historical StockX records, scrub currency characters (`$`, commas), cast prices to numeric, compute `days_since_release`, and remove invalid entries. | Clean dataset saved to `data/processed/clean_stockx.csv` with 0 string artifacts and verified numerical price columns. |
| **O2** | **Feature Preprocessing & Single Model Training (Phases 2 & 3):** Prepare features (`brand`, `retail_price`, `shoe_size`, `days_since_release`) and train a single `RandomForestRegressor` predicting resale price. | Model successfully trains in $< 2\text{ minutes}$ with cross-validated $R^2 > 0.70$ and exported inference artifact `models/best_model.joblib`. |
| **O3** | **Export & Evaluation Handoff:** Export serialized model pipeline and a test set sample check table for downstream API integration and evaluation. | `models/best_model.joblib` loads and predicts in $< 50\text{ ms}$; `data/processed/test_predictions.csv` generated with true vs. predicted prices. |

---

## 📌 4. Project Scope (Harsh Kumar's Responsibilities)

### Core Scope (Essential for 16–18 November Demonstration)
1. **Data Cleaning (`src/data_prep.py`):**
   - Parse StockX dataset (`data/raw/`).
   - Remove currency formatting (`$`, `,`) and cast `Sale Price` and `Retail Price` to `float64`.
   - Calculate elapsed time: $\text{days\_since\_release} = (\text{Order Date} - \text{Release Date})$.
   - Filter non-physical records (where `Sale Price <= 0`).
2. **Feature Preprocessing & Model Pipeline (`src/train.py`):**
   - Handle categorical features (`brand`) using standard scikit-learn encoders.
   - Scale continuous inputs (`retail_price`, `days_since_release`, `shoe_size`).
   - Train a single baseline **Random Forest Regressor** (`RandomForestRegressor(n_estimators=100, random_state=42)`).
3. **Model Serialization & Downstream Handoff:**
   - Serialize the trained pipeline to `models/best_model.joblib`.
   - Export sample verification rows to `data/processed/test_predictions.csv` for Anamika Ghosh (Phase 4).
   - Provide Sinthoiba Kangjam (Phase 5) with the exact dictionary input specification.

### Optional Enhancements (Non-Core / Time-Permitting)
- Benchmarking against a second algorithm (`GradientBoostingRegressor`).
- Hyperparameter tuning via `GridSearchCV`.
- Out-of-fold target encoding for granular sneaker silhouettes.
- Interactive residual diagnostic charts.

---

## 📌 5. Functional Requirements (Harsh Kumar's Ownership)

| ID | Functional Requirement | Priority | Acceptance Condition / How It Will Be Tested |
| :--- | :--- | :--- | :--- |
| **FR-01** | The data ingestion script shall clean raw StockX transaction data into valid numerical types and compute `days_since_release`. | **Must** | Running `python src/data_prep.py` produces `data/processed/clean_stockx.csv` with zero nulls and correct data types. |
| **FR-02** | The system shall train a single `RandomForestRegressor` pipeline predicting sneaker resale price directly. | **Must** | `python src/train.py` trains the pipeline and logs train/test evaluation metrics without errors. |
| **FR-03** | The system shall export the trained pipeline as a self-contained `joblib` file. | **Must** | `models/best_model.joblib` exists on disk; loading the file and passing a test dictionary returns an estimated resale price within 50 ms. |
| **FR-04** | The system shall generate a sample verification dataset with actual vs. predicted values. | **Must** | `data/processed/test_predictions.csv` contains columns `[actual_resale_price, predicted_resale_price, retail_price, profit_or_loss]`. |
| **FR-05** | *(Optional Enhancement)* The system may compare the primary model against `GradientBoostingRegressor`. | **Could** | Optional script `src/model_comparison.py` outputs comparative MAPE/MAE scores. |

---

## 📌 6. System Design & Algorithmic Architecture

### Core Workflow
```
[StockX Data] ──> [Cleaning & days_since_release] ──> [Feature Scaling & Encoding]
                                                              │
                                                              ▼
                                              [Single RandomForestRegressor]
                                                              │
                                                              ▼
                                            [Export: models/best_model.joblib]
                                                              │
                                ┌─────────────────────────────┴─────────────────────────────┐
                                ▼                                                           ▼
                 [FastAPI: /predict endpoint]                               [Test Sample CSV: test_predictions.csv]
                 (Sinthoiba - Phase 5)                                      (Anamika - Phase 4)
```

---

## 📌 7. Dataset, Inputs and Data Management

| Item | Verified Response |
| :--- | :--- |
| **Dataset Name** | StockX Sneaker Data Contest Dataset (2019) |
| **Source / Provider** | Hosted publicly on Kaggle (Originally released by StockX LLC) |
| **Source URL** | https://www.kaggle.com/datasets/hudsonstuck/stockx-data-contest |
| **Access Date** | **15 November 2026** |
| **Licence & Usage Terms** | Publicly accessible dataset on Kaggle released for educational, data contest, and academic research purposes. Intended strictly for student project demonstration. |
| **Privacy / Safety** | Fully anonymized historical secondary sales transactions. Contains no personally identifiable information (PII), customer names, payment details, or street addresses. Geographic data is restricted to US State level. |

---

## 📌 8. Applied ML & Algorithmic Approach

| Stage | Revised Approach (Core Scope) |
| :--- | :--- |
| **Problem Type** | Tabular regression predicting a single continuous target: **Resale Price** ($P_{\text{resale}}$). |
| **Target Variable Consistency** | The model strictly predicts estimated **Resale Price** ($\hat{P}_{\text{resale}}$). Estimated profit or loss is calculated directly downstream: $$\text{Profit / Loss} = \hat{P}_{\text{resale}} - P_{\text{retail}}$$ |
| **Core Model Selection** | **Random Forest Regressor (`RandomForestRegressor`):** A robust ensemble of decision trees that handles non-linear relationships, resists overfitting, requires minimal parameter tuning, and trains within 2 minutes. |
| **Model Serving / Integration** | Pipeline is exported to `models/best_model.joblib`. When given drop parameters (`brand`, `retail_price`, `shoe_size`, `days_since_release`), it outputs the estimated resale price and calculated profit/loss. |
| **Academic Limitations & Disclaimer** | **The estimate is based on historical StockX data from 2017–2019. It may not match today’s prices and is for a student project demonstration, not financial advice or a buy/sell recommendation.** |

---

## 📌 9. Team Confirmation
| Student Name | Signature / Acknowledgement | Date |
| :--- | :--- | :--- |
| **Harsh Kumar** (Sl. No. 31) | *[Harsh Kumar]* | 16-11-2026 |
