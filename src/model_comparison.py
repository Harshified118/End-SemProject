"""
DropOrCop - Optional Model Comparison (FR-05)
Author: Harsh Kumar (Sl. No. 31) - ML Lead
Compares baseline RandomForestRegressor vs GradientBoostingRegressor
"""

import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def run_model_comparison(data_path: Path = Path("data/processed/clean_stockx.csv")):
    """Train and benchmark RandomForestRegressor vs GradientBoostingRegressor."""
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)

    feature_cols = ["brand", "retail_price", "shoe_size", "days_since_release"]
    target_col = "sale_price"

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    models = {
        "RandomForestRegressor": RandomForestRegressor(
            n_estimators=100, max_depth=12, min_samples_leaf=5, random_state=42, n_jobs=-1
        ),
        "GradientBoostingRegressor": GradientBoostingRegressor(
            n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42
        ),
    }

    results = []

    for name, regressor in models.items():
        print(f"\nTraining {name}...")
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), ["brand"]),
                ("num", StandardScaler(), ["retail_price", "shoe_size", "days_since_release"]),
            ]
        )
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", regressor)])

        t_start = time.time()
        pipeline.fit(X_train, y_train)
        train_time = time.time() - t_start

        y_pred = pipeline.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        results.append(
            {
                "Model": name,
                "Train Time (s)": round(train_time, 2),
                "R² Score": round(r2, 4),
                "MAE ($)": round(mae, 2),
                "MAPE (%)": round(mape * 100, 2),
                "RMSE ($)": round(rmse, 2),
            }
        )

    results_df = pd.DataFrame(results)
    print("\n================ 🏆 MODEL BENCHMARK RESULTS 🏆 ================")
    print(results_df.to_string(index=False))

    output_csv = Path("reports/model_comparison_results.csv")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_csv, index=False)
    print(f"\nSaved benchmark results to: {output_csv}")
    return results_df


if __name__ == "__main__":
    run_model_comparison()
