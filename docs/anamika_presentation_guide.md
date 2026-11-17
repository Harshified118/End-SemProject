# DropOrCop: Phase 4 Presentation & Viva Guide
**Author / Presenter:** Anamika Ghosh  
**Role:** Model Checking & Evaluation Lead (Group G, Roll No. 32)  
**Academic Context:** Department of Computer Science & Engineering | B.Tech CSE End-Semester Project (Nov 2026)  
**Faculty Mentor:** Megha Gupta  

---

## 1. How Phase 4 Works (In Plain English)

Using our restaurant analogy:
* **Harsh (ML Lead):** Cooked the meal (trained the Random Forest model on 80% of our sneaker data).
* **Anamika (Evaluation Lead - Phase 4):** I am the **food critic and quality control inspector**. My job was to take the remaining 20% of sneakers the model had never seen before (18,871 actual StockX sales), test the model's predictions against reality, calculate mathematical error metrics (MAE, RMSE, MAPE, $R^2$), check for errors or bias, and certify whether the predictions are safe and reliable for real users.
* **Sinthoiba (Backend Lead):** Serves the certified predictions through the FastAPI waiter.
* **Himesh (Frontend Lead):** Shows the results cleanly on the web application menu.

---

## 2. Key Numbers Every Examiner Expects You to Know (Memorize These!)

| Metric | Value | What It Means in Simple English |
| :--- | :---: | :--- |
| **Test Set Size ($N$)** | **18,871** | The number of holdout transactions used for validation. |
| **$R^2$ Score** | **0.6525** | The model explains **65.25% of the price variance** in secondary sneaker sales. |
| **MAE (Mean Absolute Error)** | **$88.69** | On average, predictions are off by ~$88 from actual selling price. |
| **RMSE (Root Mean Squared Error)** | **$143.71** | Penalizes rare, extreme viral auctions heavily. |
| **MAPE (Percentage Error)** | **20.23%** | Average relative accuracy is ~80%. |
| **COP/DROP Verdict Accuracy** | **99.02%** | Correctly classifies whether a shoe is profitable 99 times out of 100. |
| **Residual Mean (Bias)** | **-$1.22** | Near-zero bias; the model does not systematically over- or under-estimate. |

---

## 3. Word-for-Word Presentation Script

*(Practice this out loud. It takes approximately 2 minutes to deliver confidently during your PPT presentation.)*

---

### **Slide: Phase 4 – Model Validation, Residual Diagnostics & Error Analysis**

> *"Good morning / afternoon everyone and respected faculty members. My name is **Anamika Ghosh**, and I am the **Model Checking and Evaluation Lead** for Group G.*
>
> *Once Harsh finished training our Random Forest regression pipeline, my responsibility in **Phase 4** was to conduct a rigorous, independent quality check on **18,871 unseen holdout test transactions** to determine whether our model generalizes well to real-world sneaker markets.*
>
> *Here is what my evaluation revealed across our four core diagnostics:*
>
> 1. *First, looking at explanatory power: our model achieved an **$R^2$ score of 0.6525**, meaning our pipeline captures **65.25% of the total price variance** using just four physical features (`brand`, `retail_price`, `shoe_size`, and `days_since_release`). In the context of secondary fashion markets where celebrity hype is volatile, 65% is a very strong, realistic result.*
>
> 2. *Second, measuring prediction error: we calculated a **Mean Absolute Error (MAE) of $88.69** and an **RMSE of $143.71**. When comparing brands, we found that **Yeezy** models have a tighter absolute error of **$78**, whereas **Off-White** models have higher dollar variance because individual collaboration pairs often resell for upwards of $1,000.*
>
> 3. *Third, on residual diagnostics: I plotted our prediction error distribution and confirmed that our **residual mean is -$1.22**, which is practically zero. This proves mathematically that our model has **no systematic upward or downward bias**.*
>
> 4. *Finally, when we evaluate business utility: our **directional COP/DROP verdict accuracy reached 99.02%**. This means that even when a dollar prediction has slight variance, the investment recommendation—whether a sneaker will resell above retail or at a loss—is correct 99% of the time.*
>
> *I also investigated our edge cases and outliers, confirming that depth regularization (`max_depth=12`) successfully prevented overfitting while delivering sub-millisecond latency for Sinthoiba's backend API. Thank you."*

---

## 4. Top Examiner Viva Questions & Answers (Cheat Sheet)

### **Q1: Why is your $R^2$ 0.65 and not 0.90+?**
> **Answer:** *"Secondary sneaker resale is governed by unpredictable human psychology—celebrity endorsements, sudden restocks by Adidas or Nike, and micro-influencer trends—which cannot be captured by tabular physical features alone. An $R^2$ of 0.65 is statistically solid for this domain; if our test $R^2$ were 0.95 with only four features, it would almost certainly indicate data leakage or severe overfitting."*

### **Q2: Why did you report both MAE and RMSE? Which is more relevant?**
> **Answer:** *"Both are essential. MAE ($88.69) is linear and tells us the average dollar error on a typical sneaker. RMSE ($143.71) squares errors before taking the root, heavily penalizing large outliers. The fact that RMSE is higher than MAE demonstrates that our largest errors are concentrated in a few viral hype grails (like Off-White Chicagos), while everyday sneakers have much lower error."*

### **Q3: What are residuals, and what did your residual plot tell you?**
> **Answer:** *"A residual is simply the actual price minus the predicted price: $e_i = y_i - \hat{y}_i$. In our residual histogram (`reports/figures/02_residual_distribution.png`), the errors follow a normal bell curve centered at -$1.22. This confirms our model is unbiased. In our scatter plot (`reports/figures/03_residuals_vs_predicted.png`), we observed mild heteroscedasticity—meaning variance increases for sneakers above $800, which is expected for luxury collector items."*

### **Q4: How did you test for overfitting (bias-variance tradeoff)?**
> **Answer:** *"We tested unconstrained trees (`max_depth=None`), which scored 0.98 on training but dropped to 0.58 on the test set, proving severe variance. By tuning the model to `max_depth=12` and `min_samples_leaf=5`, we closed the train-test gap, boosted test $R^2$ to 0.65, and kept inference latency under 0.1 milliseconds."*

### **Q5: How can your COP/DROP accuracy be 99% when $R^2$ is only 65%?**
> **Answer:** *"Regression measures continuous numerical proximity (how close the dollar amount is), while COP/DROP classification measures directional profitability (whether price is greater than retail). Even if the model predicts an $800 sneaker will sell for $720, both numbers are well above its $190 retail price, correctly yielding a COP verdict."*
