# PRD Section Entries: Harsh Kumar (Sl. No. 31) [REVISED & CORRECTED]
**Project Title:** DropOrCop: Sneaker & Streetwear Resale Profit Predictor  
**Group:** Group G  
**Faculty Mentor:** Megha Gupta  
**Assigned Ownership:** Team Leader & ML Lead: Clean the dataset, prepare features and train the single RandomForestRegressor model (Phases 1, 2, 3)  
**Revision Date:** 16-11-2026 / 17-11-2026 (Corrected Submission Draft per Faculty Review)  
**Target Document:** `DropOrCop_PRD_Group_G_Corrected_17Nov2026.docx` / `docs/PRD_DropOrCop_Group_G.docx`  

---

## 📌 Document & Team Details

### Team and Project Details (Table 1)
| Field | Team Response |
| :--- | :--- |
| **Group ID** | Group G |
| **Assigned Project Title** | DropOrCop: Sneaker & Streetwear Resale Profit Predictor |
| **Programme / Course / Semester** | B.Tech in Computer Science & Engineering / End-Semester Project Assessment (November 2026) |
| **Project Window** | 16–20 November 2026 (Project work: 16–18 November; PPT presentations: 19–20 November) |
| **Faculty Mentor** | Megha Gupta |
| **Team Leader / Coordinator** | Harsh Kumar (Sl. No. 31) |
| **PRD Submission Date** | 16-11-2026 (Resubmission Draft) |
| **Status** | Revised Working Draft for Faculty Approval (Resubmission Draft - 16 November 2026) |

### Team Member Register (Table 2)
| No. | Student Name | Role / Responsibility |
| :---: | :--- | :--- |
| **1** | **Harsh Kumar** (Sl. No. 31) | **Team Leader & ML Lead:** Clean the dataset, prepare features and train the single RandomForestRegressor model. |
| **2** | **Anamika Ghosh** (Sl. No. 32) | **Model Checking Lead:** Create the single train/test split, review a few held-out predictions and report the selected evaluation results. |
| **3** | **Sinthoiba Kangjam** (Sl. No. 34) | **Backend / Integration Lead:** Connect the trained model to the prediction workflow and support integration with the webpage. |
| **4** | **Himesh Vaskar** (Sl. No. 35) | **Frontend / UI Lead:** Build the simple webpage form and display estimated resale price, profit/loss and COP/DROP result. Optional catalog features only if time permits. |

---

## 📌 1. Project Summary
*PRD Section 1 Table Entry:*

> DropOrCop is a machine-learning web application that helps sneaker buyers and casual collectors estimate whether a sneaker resale price may be above or below its retail price. Using historical StockX secondary-market transactions (Nike x Off-White and Adidas Yeezy releases, 2017–2019), the project cleans price data, calculates `days_since_release` and prepares the selected input features. A single `RandomForestRegressor` is trained to estimate resale price using one train/test split. The team will review a few held-out predictions and record a basic evaluation summary; additional metrics, cross-validation, baseline comparisons and residual checks are optional. A simple webpage will let users enter sneaker details and view the estimated resale price, estimated profit/loss and COP/DROP result. The three-day implementation prioritises data cleaning, training and checking one Random Forest model, and completing this basic webpage. Catalog, search, save/unsave and product-detail preview features are optional only if time permits. The system is an academic prototype, not financial advice.

---

## 📌 2. Background and Problem Statement
*PRD Section 2 Table Entry:*

> Limited-edition sneakers often resell on secondary marketplaces at prices well above or below their retail price. Buyers and casual collectors have little data-backed way to tell whether a drop will appreciate or fall below retail, so they risk overpaying or losing money on a purchase. Current approaches rely on manually checking past sales and listings, which is slow and gives no direct estimate of profit or loss for a given retail price. DropOrCop addresses this by training a regression model on historical secondary-market transactions to estimate resale value and give an immediate, data-backed profit-or-loss indication with a COP/DROP verdict before purchase.

---

## 📌 3. Aim, Objectives and Success Indicators
*PRD Section 3 Table Entry:*

**Overall Aim:**  
> **"The aim of DropOrCop is to make a simple website that uses past sneaker sales to estimate a sneaker’s resale price and possible profit or loss."**

### Project Objectives & Success Indicators
| Objective ID | Objective Description | Measurable Success Indicator |
| :---: | :--- | :--- |
| **O1** | **Data Cleaning:** Ingest historical StockX records, remove currency formatting, convert prices to numeric values, calculate `days_since_release` and remove invalid entries. | A cleaned dataset is saved (`data/processed/clean_stockx.csv`) with numeric price columns and documented cleaning checks. |
| **O2** | **Single-Model Training:** Prepare the selected features and train one `RandomForestRegressor` to predict resale price. | The model trains successfully and the exported pipeline (`models/best_model.joblib`) is available for prediction. |
| **O3** | **Model Checking:** Use one train/test split, generate a few predictions on held-out records and review the results. | A small set of sample predictions and a basic evaluation summary are recorded (`data/processed/test_predictions.csv`). Extra metrics, cross-validation, baseline comparisons and residual checks are optional. |
| **O4** | **Simple Webpage:** Build a basic webpage that accepts sneaker details and displays estimated resale price, estimated profit/loss and the COP/DROP result. | A valid input produces and displays all three outputs. |

---

## 📌 4. Project Scope

### Included in Scope — Essential Three-Day Work (16–18 November 2026)
1. **Data Cleaning (Harsh Kumar):** Clean the supplied StockX dataset, convert price fields to numeric values, calculate `days_since_release`, and remove invalid records.
2. **Feature Preparation and Single-Model Training (Harsh Kumar):** Prepare the selected input features (`brand`, `retail_price`, `shoe_size`, `days_since_release`) and train one `RandomForestRegressor` to estimate resale price.
3. **Model Checking (Anamika Ghosh):** Use one train/test split, check a few held-out predictions and record a basic evaluation summary. Additional metrics, five-fold cross-validation, baseline comparisons and residual checks are optional.
4. **Simple Webpage and Integration (Sinthoiba Kangjam and Himesh Vaskar):** Connect the trained model to a basic webpage that displays estimated resale price, estimated profit/loss and the COP/DROP result.
5. **Testing and Presentation (All four members):** Run a few end-to-end test inputs, prepare the PPT, and document the results.

### Optional Enhancements (Non-Core / Only If Time Permits)
* **Sample sneaker catalog, search, save/unsave, and product detail preview:** These are not required for completion of the core three-day scope.
* **Optional additional model checks:** Five-fold cross-validation, comparison with naive or brand-median baselines, extra evaluation measures (MAPE, $R^2$), residual diagnostics, secondary algorithm benchmark (`GradientBoostingRegressor`), and hyperparameter grid searching.

### Assumptions, Constraints & Dependencies
1. **Dataset:** Pre-collected Kaggle StockX 2019 dataset (no live web scraping required).
2. **Timeframe:** Three-day development window (16–18 November 2026); priority is data cleaning, one Random Forest model, model checking, and a simple webpage.
3. **Hardware & Serving:** Local execution using the available development environment; no paid cloud service or API key is required.
4. **Libraries:** Python 3.10+, pandas, NumPy, scikit-learn, joblib, FastAPI, Uvicorn, Node.js, React, and Vite.
5. **Optional Frontend Extras:** Catalog, search, save/unsave, and product detail preview may be omitted.
6. **Key Risks:** Model accuracy may be limited by the small feature set and historical 2017–2019 data; report evaluation results and limitations clearly.

---

## 📌 5. Users / Project Requirements

### 5.1 Functional Requirements (FR-01 to FR-13)
| ID | Functional Requirement | Priority | Acceptance Condition / How It Will Be Tested |
| :--- | :--- | :---: | :--- |
| **FR-01** | The data ingestion script shall clean raw StockX transaction data into valid numerical types and compute `days_since_release`. | **Must** | Running `python src/data_prep.py` produces `clean_stockx.csv` with zero nulls and correct data types. |
| **FR-02** | The system shall train a single `RandomForestRegressor` pipeline predicting sneaker resale price directly. | **Must** | `python src/train.py` trains the pipeline and logs train/test evaluation metrics without errors. |
| **FR-03** | The system shall export the trained pipeline as a self-contained `joblib` file. | **Must** | `models/best_model.joblib` exists on disk; loading the file and passing a test dictionary returns an estimated resale price within 50 ms. |
| **FR-04** | The system shall generate a sample verification dataset with actual vs. predicted values. | **Must** | A few held-out examples are recorded with their predicted values; no claim of measured speed is required. |
| **FR-05** | The backend or local prediction workflow shall provide the model estimate to the webpage. | **Must** | The webpage receives valid input and displays the estimated resale price, profit/loss and COP/DROP result. |
| **FR-06** | The frontend shall provide a prediction form where users enter brand, retail price, shoe size and days since release, and display the predicted resale price, estimated profit/loss and COP/DROP verdict returned by the API. | **Must** | Submitting valid inputs calls `POST /predict` and renders the resale price, profit/loss and a COP ($\text{profit} > 0$) or DROP ($\text{profit} \le 0$) badge; invalid inputs show a descriptive error banner without crashing. |
| **FR-07** | The webpage may display a sample sneaker catalog if time permits. | **Could-have** | If implemented, sample records are clearly labelled illustrative and are separate from live model predictions. |
| **FR-08** | The webpage may provide catalog search if time permits. | **Could-have** | If implemented, search filters the optional sample catalog. |
| **FR-09** | The webpage may allow session save/unsave if time permits. | **Could-have** | If implemented, save/unsave state toggles during the browser session. |
| **FR-10** | The webpage may provide a product detail preview if time permits. | **Could-have** | If implemented, the preview clearly labels any illustrative information. |
| **FR-11** | The frontend shall provide fully responsive layouts for mobile, tablet, and desktop screens. | **Must** | CSS flexbox/grid layout adapts cleanly to screen widths from 375px to 1920px without horizontal scrolling. |
| **FR-12** | Optional: the team may calculate additional metrics, run five-fold cross-validation, compare baselines or inspect residuals if time permits. | **Could-have** | Any additional checks completed are documented; they are not required for the core demonstration. |
| **FR-13** | Optional enhancement: compare the Random Forest model with another model only if the core work is complete. | **Could-have** | A comparison is included only if time permits. |

### 5.2 Non-Functional Requirements
| Area | Requirement for This Project |
| :--- | :--- |
| **Usability** | Simple, clear user flow with readable input labels and visible prediction outputs. |
| **Performance** | Target: single-instance model inference latency below 50 ms; FastAPI round-trip response below 100 ms. These are performance targets, not measured results. Catalog search performance is not part of the core scope. |
| **Reliability** | Frontend and backend handle missing fields, invalid types, out-of-range values (e.g., negative days or shoe size), and API network disconnects gracefully with descriptive fallback banners, avoiding crashes. |
| **Security and Privacy** | Fully anonymized public dataset containing zero personal identifiable information (PII). No user logins, passwords, or secrets stored in client-side code. |
| **Compatibility** | Web application fully functional across modern desktop and mobile browsers (Google Chrome, Mozilla Firefox, Safari, Microsoft Edge). Compatible with standard Python 3.10+ and Node.js environments. |
| **Maintainability** | Codebase adopts modular directory structure (`src/data_prep.py`, `src/train.py`, `api/main.py`, `frontend/`), clean component separation, and comprehensive documentation. |

---

## 📌 6. Proposed Solution & System Design

### Architecture Workflow
```
[StockX Dataset] ──> [Data Cleaning] ──> [Feature Preparation] ──> [Single RandomForestRegressor]
                                                                                │
                                                                                ▼
                                                        [One Train/Test Split + Sample Prediction Checks]
                                                                                │
                                                                                ▼
                                                                [Saved Model / Prediction Workflow]
                                                                (models/best_model.joblib)
                                                                                │
                                                                                ▼
                                                                         [Simple Webpage]
                                                   Displays: Estimated Resale Price | Profit/Loss | COP/DROP
```

### 6.1 Modules and Responsibilities
| Module | Purpose / Main Functions | Owner (Member ID) |
| :--- | :--- | :--- |
| **Data Ingestion & Cleaning (Phase 1)** | Ingest StockX dataset, clean currency strings, compute `days_since_release`, filter invalid prices | Harsh Kumar (Sl. No. 31) |
| **Feature Preprocessing & Model Training (Phases 2 & 3)** | Preprocess features (`OneHotEncoder` for brand, `StandardScaler`), train single `RandomForestRegressor`, export `best_model.joblib` | Harsh Kumar (Sl. No. 31) |
| **Model Evaluation & Verification (Phase 4)** | Use one train/test split, review a few held-out predictions and record a basic evaluation summary. Optional: additional metrics, cross-validation, baseline comparisons and residual checks. | Anamika Ghosh (Sl. No. 32) |
| **Backend / API Serving (Phase 5)** | FastAPI REST microservice (`api/main.py`), routes (`/predict`, `/brands`, `/health`), Pydantic validation schemas, CORS middleware, model serving | Sinthoiba Kangjam (Sl. No. 34) |
| **Frontend / UI (Phase 6)** | React and Vite webpage: prediction form showing estimated resale price, profit/loss and COP/DROP result. Catalog, search, save/unsave and detail preview are optional. | Himesh Vaskar (Sl. No. 35) |
| **Testing & Presentation** | Run a few end-to-end test inputs, prepare the presentation slides and document the demonstration. | All four members (Group G) |

### 6.2 Technology Stack
| Layer | Chosen Tool / Technology | Reason for Selection |
| :--- | :--- | :--- |
| **Frontend Framework & UI** | React, JavaScript, CSS | Component-based webpage and a straightforward prediction form. |
| **Build & Development Tool** | Vite | Fast Hot Module Replacement (HMR), quick local server startup, and an optimized ES modules build pipeline. |
| **UI Icons** | Lucide React | Consistent icons for the basic prediction interface. |
| **Backend Framework & Server** | Python 3.10+, FastAPI, Uvicorn | Asynchronous REST API framework with native Pydantic schema validation, CORS support, and automatic OpenAPI documentation. |
| **ML & Data Processing** | scikit-learn, pandas, NumPy | Vectorized tabular operations over 94,000 rows; robust tree-based `RandomForestRegressor` ensemble. |
| **Model Serialization** | joblib | Industry standard for serializing scikit-learn tree ensembles, allowing fast loading and sub-millisecond inference in FastAPI. |
| **Development & Version Control** | Visual Studio Code, Git, GitHub | Standardized cross-team development environment with branch-based version control; per-member commits serve as evidence of individual contribution. |
| **Hosting & Serving (Local Setup)**| Localhost ASGI (:8000) & Vite (:5173) | High reliability, zero external hosting latency, and fully reproducible execution during academic demonstration. |

---

## 📌 7. Dataset, Inputs and Data Management

| Item | Team Response / Verified Detail |
| :--- | :--- |
| **Dataset / Source Name** | StockX Sneaker Data Contest Dataset (2019) |
| **Source URL / Provider** | https://www.kaggle.com/datasets/hudsonstuck/stockx-data-contest (Hosted publicly on Kaggle, originally released by StockX LLC) |
| **Access Date & Licence Terms** | **Access Date:** 15 November 2026. **Licence shown on the Kaggle dataset page:** Unknown. The dataset page does not specify a licence; public availability on Kaggle should not be treated as a licence. Released for educational, data contest, and academic demonstration. |
| **Privacy / Safety Measures** | Fully anonymized historical secondary sales transactions (99,956 raw records; approximately 94,000 retained after cleaning). Contains no personally identifiable information (PII), customer names, payment details, or street addresses. Geographic data is restricted to US State level. |
| **External Code / GenAI Disclosure** | Project libraries/tools listed in this PRD: pandas, NumPy, scikit-learn, joblib, FastAPI, Uvicorn, React, Vite and Lucide React. **Generative-AI disclosure:** ChatGPT (OpenAI) was used to assist with revision of this PRD text. The team has not reported using generative AI to generate project code. No external code snippets have been identified in the information supplied for this revision. |

---

## 📌 8. Applied ML & Algorithmic Approach

| Stage | Planned Approach / Decision (Core vs. Optional) |
| :--- | :--- |
| **Problem Type** | Tabular regression predicting a single continuous target: **Resale Price** ($P_{\text{resale}}$). |
| **Target Consistency & Verdict Rule** | The model strictly predicts estimated Resale Price ($P_{\text{resale}}$); estimated net profit/loss is calculated downstream as $(\hat{P}_{\text{resale}} - P_{\text{retail}})$. **Verdict Rule:** **COP** if estimated $\text{profit/loss} > 0$ (estimated resale price exceeds retail price); otherwise **DROP**. |
| **Preprocessing** | 1. Currency string cleansing (`$` and commas removed, cast to `float64`).<br>2. Temporal feature generation: $\text{days\_since\_release} = (\text{Order Date} - \text{Release Date})$.<br>3. Removal of invalid records (where `Sale Price <= 0` or negative release days). |
| **Feature Engineering** | Categorical encoding for `brand` (One-Hot Encoding); standard scaling for continuous features (`retail_price`, `shoe_size`, `days_since_release`) assembled into an encapsulated scikit-learn pipeline. |
| **Baseline** | **Not required for the core three-day project.** Optional only if time permits: compare against a naive or brand-median baseline. |
| **Candidate Model(s) / Algorithm** | **Primary model:** Random Forest Regressor (`RandomForestRegressor`), configured as an ensemble of 100 decision trees. **Training-time goal:** under 2 minutes; this is a target, not a measured result. |
| **Training / Validation Plan** | Use **one 80/20 train/test split** with a fixed random seed (`random_state=42`). Five-fold cross-validation is optional and not required for the three-day scope. |
| **Evaluation Metrics** | **Core:** Review a few held-out predictions and report a basic evaluation summary using MAE and RMSE where feasible.<br>**Optional:** MAPE, $R^2$, baseline comparisons and residual diagnostics. |
| **Model Serving / Integration** | The trained pipeline is intended to be connected to the simple webpage. **Target inference latency:** below 50 ms; this is a target, not a measured result. The webpage displays estimated resale price, estimated profit/loss and COP/DROP result. Catalog, search, save/unsave and product detail preview are optional and may be omitted. |
| **Academic Limitations & Responsible Use**| **The estimate is based on historical StockX data from 2017–2019. It may not match today’s prices, uses only four input features (brand, retail price, shoe size, days since release) and does not account for sneaker model or colourway. It is for a student project demonstration, not financial advice or a buy/sell recommendation.** |

---

## 📌 9. Team Confirmation

| Student Name | Role | Acknowledgement | Date |
| :--- | :--- | :---: | :---: |
| **Harsh Kumar** (Sl. No. 31) | Team Leader & ML Lead | Harsh Kumar | 16-11-2026 |
| **Anamika Ghosh** (Sl. No. 32) | Model Checking Lead | Anamika Ghosh | 16-11-2026 |
| **Sinthoiba Kangjam** (Sl. No. 34) | Backend / Integration Lead | Sinthoiba Kangjam | 16-11-2026 |
| **Himesh Vaskar** (Sl. No. 35) | Frontend / UI Lead | Himesh Vaskar | 16-11-2026 |

*Faculty Review Status:* Revised Working Draft for Faculty Approval (Resubmission Draft). Faculty Mentor: Megha Gupta.
