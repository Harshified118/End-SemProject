"""
DropOrCop - Phase 2 & 3: Feature Preprocessing & Model Training
Author: Harsh Kumar (Sl. No. 31) - ML Lead
"""

import os
import time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def train_and_export_model(
    data_path: Path = Path("data/processed/clean_stockx.csv"),
    model_output_path: Path = Path("models/best_model.joblib"),
    test_pred_output_path: Path = Path("data/processed/test_predictions.csv"),
    random_state: int = 42,
) -> Pipeline:
    """Train RandomForestRegressor pipeline, evaluate, and export artifacts."""
    print(f"Loading processed dataset from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")

    # Core feature definition per PRD and Handoff contract
    feature_cols = ["brand", "retail_price", "shoe_size", "days_since_release"]
    target_col = "sale_price"

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    # Train / Test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=random_state
    )
    print(f"Training set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples")

    # Preprocessor: OneHotEncoder for brand, StandardScaler for numerical inputs
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), ["brand"]),
            ("num", StandardScaler(), ["retail_price", "shoe_size", "days_since_release"]),
        ]
    )

    # Scikit-learn Pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    max_depth=12,
                    min_samples_leaf=5,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("Training RandomForestRegressor pipeline...")
    t_start = time.time()
    pipeline.fit(X_train, y_train)
    t_train = time.time() - t_start
    print(f"Training completed in {t_train:.2f} seconds.")

    # Evaluate on test set
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\n--- 📊 Evaluation Metrics on Test Set ---")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE (Mean Absolute Error): ${mae:.2f}")
    print(f"MAPE (Mean Absolute Percentage Error): {mape * 100:.2f}%")
    print(f"RMSE (Root Mean Squared Error): ${rmse:.2f}")

    # Export serialized model pipeline
    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_output_path)
    print(f"\nModel artifact serialized to: {model_output_path}")

    # Generate test predictions handoff dataset for Phase 4 (Anamika Ghosh)
    test_handoff = pd.DataFrame(
        {
            "actual_resale_price": np.round(y_test.values, 2),
            "predicted_resale_price": np.round(y_pred, 2),
            "retail_price": np.round(X_test["retail_price"].values, 2),
            "profit_or_loss": np.round(y_pred - X_test["retail_price"].values, 2),
        }
    )
    test_pred_output_path.parent.mkdir(parents=True, exist_ok=True)
    test_handoff.to_csv(test_pred_output_path, index=False)
    print(f"Test predictions exported to: {test_pred_output_path} ({len(test_handoff)} rows)")

    # Verify inference latency on single sample (< 50ms requirement)
    sample_payload = pd.DataFrame(
        [
            {
                "brand": "Yeezy",
                "retail_price": 220.0,
                "shoe_size": 10.5,
                "days_since_release": 45,
            }
        ]
    )
    t0 = time.perf_counter()
    sample_pred = pipeline.predict(sample_payload)[0]
    latency_ms = (time.perf_counter() - t0) * 1000
    print(f"\nInference Benchmark:")
    print(f"Sample Input: {sample_payload.to_dict(orient='records')[0]}")
    print(f"Predicted Resale Price: ${sample_pred:.2f}")
    print(f"Inference Latency: {latency_ms:.2f} ms (< 50 ms threshold: {'PASS' if latency_ms < 50 else 'FAIL'})")

    return pipeline


if __name__ == "__main__":
    train_and_export_model()
