"""
DropOrCop - Phase 1: Data Ingestion & Cleaning
Author: Harsh Kumar (Sl. No. 31) - ML Lead
"""

import os
from pathlib import Path
import pandas as pd


def get_raw_data_path() -> Path:
    """Find the raw StockX dataset file."""
    candidates = [
        Path("data/raw/StockX-Data-Contest-2019-3.csv"),
        Path("data/raw/StockX-Data-Contest-2019.csv"),
        Path("StockX-Data-Contest-2019-3.csv"),
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Could not find StockX dataset in data/raw/ or root directory."
    )


def clean_currency(series: pd.Series) -> pd.Series:
    """Strip currency symbols and commas, convert to float64."""
    return (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype(float)
    )


def clean_stockx_data(input_path: Path, output_path: Path) -> pd.DataFrame:
    """Ingest, clean, engineer features, and export cleaned dataset."""
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path, encoding="utf-8-sig")
    print(f"Raw dataset shape: {df.shape}")

    # 1. Clean column names to snake_case
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 2. Clean string categorical columns
    df["brand"] = df["brand"].astype(str).str.strip()
    df["sneaker_name"] = df["sneaker_name"].astype(str).str.strip()
    df["buyer_region"] = df["buyer_region"].astype(str).str.strip()

    # 3. Clean and convert prices
    df["sale_price"] = clean_currency(df["sale_price"])
    df["retail_price"] = clean_currency(df["retail_price"])
    df["shoe_size"] = df["shoe_size"].astype(float)

    # 4. Parse dates
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
    df["release_date"] = pd.to_datetime(df["release_date"], format="mixed")

    # 5. Calculate elapsed release duration: days_since_release
    df["days_since_release"] = (df["order_date"] - df["release_date"]).dt.days

    # 6. Filter non-physical or corrupted records
    initial_count = len(df)
    valid_mask = (df["sale_price"] > 0) & (df["days_since_release"] >= 0)
    df_clean = df[valid_mask].copy().reset_index(drop=True)
    filtered_count = initial_count - len(df_clean)
    print(f"Filtered out {filtered_count} records with negative days or invalid price.")
    print(f"Cleaned dataset shape: {df_clean.shape}")

    # Verify zero nulls in core columns
    core_cols = ["brand", "sale_price", "retail_price", "shoe_size", "days_since_release"]
    null_counts = df_clean[core_cols].isnull().sum()
    print("Null count in core columns:\n", null_counts)
    assert null_counts.sum() == 0, f"Found unexpected null values: {null_counts}"

    # 7. Export to processed CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned data successfully exported to: {output_path}")

    return df_clean


if __name__ == "__main__":
    raw_path = get_raw_data_path()
    processed_path = Path("data/processed/clean_stockx.csv")
    clean_stockx_data(raw_path, processed_path)
