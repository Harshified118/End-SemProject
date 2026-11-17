# DropOrCop: Model Evaluation & Residual Diagnostics Report (Phase 4)

**Author:** Anamika Ghosh (Model Checking & Evaluation Lead, Group G, Sl. No. 32)  
**Academic Context:** Department of Computer Science & Engineering | B.Tech CSE End-Semester Capstone Project (November 2026)  
**Faculty Mentor:** Megha Gupta  
**Evaluation Dates:** 19–20 November 2026  
**Artifact Dependencies:** Evaluated on held-out test split (`data/processed/test_predictions.csv`, $N = 18,871$) generated from the trained Random Forest pipeline (`models/best_model.joblib`).

---

## 1. Executive Summary

In Phase 4, the primary objective is to rigorously validate the trained regression model on unseen test data, analyze error behavior, detect systematic bias or heteroscedasticity, and assess directional accuracy for the COP/DROP investment recommendation.

The evaluation was performed across **18,871 held-out test transactions** (an 80/20 train/test split with `random_state=42`). 

### Core Evaluation Findings:
* **Coefficient of Determination ($R^2$):** `0.6525` (The Random Forest explains **65.25% of the total variance** in sneaker secondary market resale pricing).
* **Mean Absolute Error (MAE):** **$88.69** (On average, predicted resale prices deviate by ~$88 from actual transaction prices).
* **Root Mean Squared Error (RMSE):** **$143.71** (Larger than MAE due to high penalties on rare, extreme luxury hype spikes).
* **Mean Absolute Percentage Error (MAPE):** **20.23%** (Predictions maintain an average 80% pricing precision relative to sale value).
* **COP/DROP Verdict Directional Accuracy:** **99.02%** (The model correctly recommends COP or DROP in over 99 out of 100 cases).
* **Mean Residual (Systematic Bias):** **-$1.22** (Virtually unbiased; the error distribution is centered at zero).

---

## 2. Comprehensive Metric Breakdown

| Metric | Overall Test Set | Yeezy Subset ($N=13,917$) | Off-White Subset ($N=4,954$) | Viva Benchmark Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **$R^2$ Score** | **0.6525** | 0.3239 | 0.6172 | Moderate-to-strong explanatory power on highly volatile hype assets. |
| **MAE** | **$88.69** | **$78.11** | $118.43 | Typical dollar prediction error; Yeezy exhibits tighter absolute dispersion. |
| **RMSE** | **$143.71** | **$114.39** | $204.74 | Penalizes large errors heavily; Off-White has higher variance and extreme outliers. |
| **MAPE** | **20.23%** | 21.25% | **17.35%** | Percentage error is actually lower for Off-White due to higher baseline prices ($600–$1,200). |
| **Verdict Accuracy** | **99.02%** | 98.68% | **100.00%** | Directional accuracy classifying profitable vs. loss-making releases. |

---

## 3. Diagnostic Visualizations

All diagnostic plots were generated programmatically via `src/evaluate.py` and are stored in `reports/figures/`:

### 3.1 Actual vs. Predicted Resale Price
* **File:** `reports/figures/01_actual_vs_predicted.png`
* **Interpretation:** Test samples cluster tightly along the $45^\circ$ parity line ($y = x$) for transactions between $200 and $600 (representing over 80% of secondary market volume). For extreme luxury grails exceeding $1,000 (e.g., Off-White Air Jordan 1 Chicago), the Random Forest predicts conservatively toward the tree leaf averages, bounding downside overestimation risk.

### 3.2 Residual Distribution (Normality & Bias Check)
* **File:** `reports/figures/02_residual_distribution.png`
* **Interpretation:** Residual errors ($e_i = y_i - \hat{y}_i$) form a classic zero-centered bell curve centered at **-$1.22**, confirming that the estimator suffers from no systematic upward or downward bias. A slight right-hand tail reflects the positive skewness inherent to viral luxury sneaker auctions.

### 3.3 Residuals vs. Predicted Price (Homoscedasticity Analysis)
* **File:** `reports/figures/03_residuals_vs_predicted.png`
* **Interpretation:** Shows a characteristic "funnel" pattern (heteroscedasticity) common in financial valuation datasets: residuals remain tightly bounded ($\pm \$50$) for mainstream Yeezy 350 releases, but expand for high-value Off-White items where secondary buyer demand is driven by celebrity endorsements and collector sentiment rather than production volume.

### 3.4 Brand Performance Comparison
* **File:** `reports/figures/04_brand_performance_comparison.png`
* **Interpretation:** Direct side-by-side comparison illustrating why Yeezy yields lower absolute dollar error ($78.11 vs. $118.43) while Off-White yields lower relative percentage error (17.35% vs. 21.25%).

---

## 4. Error Diagnostics & Outlier Analysis

To explain prediction anomalies for examiners during viva, we isolated the top over-predictions and under-predictions:

### 4.1 Under-Predicted Outliers (Actual Price >> Predicted Price)
* **Top Cases:** Rare collector items such as *Off-White Nike Air Jordan 1 Retro High Chicago* and *Off-White Air Presto White*.
* **Actual Resale:** $1,500 – $2,000+
* **Predicted Resale:** $1,000 – $1,250
* **Root Cause Analysis:** The model features (`brand`, `retail_price`, `shoe_size`, `days_since_release`) do not incorporate specific silhouette names, colorway rarity, or Virgil Abloh collaboration scarcity tiers. The tree ensemble naturally averages leaf nodes, under-predicting historical record-breaking auctions.

### 4.2 Over-Predicted Outliers (Predicted Price >> Actual Price)
* **Top Cases:** High retail price models ($300 MSRP Yeezy 700 / 750) released during market saturation phases.
* **Actual Resale:** $220 – $260
* **Predicted Resale:** $380 – $420
* **Root Cause Analysis:** The linear weight of higher retail MSRP led the model to anticipate appreciation, whereas market restocking diluted secondary premium.

---

## 5. Machine Learning Theory: Bias-Variance Tradeoff Analysis

During model selection, we evaluated the depth regularization of `RandomForestRegressor`:
1. **Unconstrained Trees (`max_depth=None`):**
   * *Training $R^2$:* 0.982 | *Test $R^2$:* 0.581 | *Latency:* > 150 ms
   * *Diagnosis:* **High Variance (Overfitting)**. Individual decision trees memorized specific transaction noise and outlier buyers.
2. **Constrained Ensemble (`max_depth=12`, `min_samples_leaf=5`):**
   * *Training $R^2$:* 0.714 | *Test $R^2$:* **0.6525** | *Latency:* **0.07 ms**
   * *Diagnosis:* **Optimal Generalization**. Enforcing minimum leaf samples smoothed leaf predictions, reduced generalization error by 7% on held-out data, and shrunk inference latency by 99%, fulfilling the PRD real-time constraint.

---

## 6. Examiner Viva Q&A Cheat Sheet for Anamika Ghosh

* **Q: Why is your $R^2$ 0.65 instead of 0.95?**  
  * *Answer:* *"Secondary sneaker pricing is driven by human sentiment, celebrity hype, and sudden restocks which are not captured in tabular features. In retail secondary market literature, an $R^2$ of 0.65 using only 4 features is considered strong and realistic. An $R^2$ of 0.95 would indicate data leakage or severe overfitting."*
* **Q: Why report both MAE and RMSE?**  
  * *Answer:* *"MAE ($88.69) treats all errors linearly and gives the expected error for typical sneakers. RMSE ($143.71) squares the errors before averaging, penalizing large errors heavily. The gap between RMSE and MAE proves that our errors are dominated by a small number of extreme high-value hype grails rather than pervasive model failure."*
* **Q: How does the model achieve 99% COP/DROP accuracy if $R^2$ is 0.65?**  
  * *Answer:* *"Because regression error and classification accuracy measure different things. Even if our predicted price misses an $800 sneaker by $90 (predicting $710 on a $190 retail shoe), the financial verdict is still correctly classified as a COP. The directional margin is robust even with moderate dollar variance."*

---

## 7. Deliverable Verification

To verify Phase 4 deliverables locally:
```bash
# Run standalone evaluation pipeline
python src/evaluate.py

# Review output figures in reports/figures/
ls -lh reports/figures/
```
