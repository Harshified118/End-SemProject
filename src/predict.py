"""
DropOrCop - Standalone Inference & Team Contract Interface
Author: Harsh Kumar (Sl. No. 31) - ML Lead
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict
import joblib
import pandas as pd

MODEL_PATH = Path("models/best_model.joblib")


def load_model(model_path: Path = MODEL_PATH):
    """Load serialized scikit-learn pipeline."""
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model artifact not found at {model_path}. Run 'python src/train.py' first."
        )
    return joblib.load(model_path)


def predict_resale(
    brand: str,
    retail_price: float,
    shoe_size: float,
    days_since_release: int,
    margin_threshold: float = 0.15,
    model=None,
) -> Dict[str, Any]:
    """
    Predict secondary resale price and deliver COP/DROP verdict.
    Contract matched with Phase 5 (Sinthoiba) and Phase 6 (Himesh).
    """
    if model is None:
        model = load_model()

    input_df = pd.DataFrame(
        [
            {
                "brand": brand,
                "retail_price": float(retail_price),
                "shoe_size": float(shoe_size),
                "days_since_release": int(days_since_release),
            }
        ]
    )

    pred_resale = float(model.predict(input_df)[0])
    pred_resale = round(pred_resale, 2)
    retail = round(float(retail_price), 2)
    estimated_profit = round(pred_resale - retail, 2)
    profit_margin_pct = round((estimated_profit / retail) * 100, 2) if retail > 0 else 0.0

    # Verdict determination based on margin threshold (default 15%)
    verdict = "COP" if (estimated_profit / retail) >= margin_threshold else "DROP"

    return {
        "brand": brand,
        "retail_price": retail,
        "shoe_size": float(shoe_size),
        "days_since_release": int(days_since_release),
        "estimated_resale_price": pred_resale,
        "estimated_profit": estimated_profit,
        "profit_margin_pct": profit_margin_pct,
        "verdict": verdict,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict sneaker resale price and profit verdict.")
    parser.add_argument("--brand", type=str, default="Yeezy", help="Sneaker brand (e.g. Yeezy, Off-White)")
    parser.add_argument("--retail", type=float, default=220.0, help="Original retail price ($)")
    parser.add_argument("--size", type=float, default=10.5, help="Shoe size (US)")
    parser.add_argument("--days", type=int, default=45, help="Elapsed days since release")
    parser.add_argument("--threshold", type=float, default=0.15, help="Profit margin threshold (e.g. 0.15 for 15 percent)")

    args = parser.parse_args()

    result = predict_resale(
        brand=args.brand,
        retail_price=args.retail,
        shoe_size=args.size,
        days_since_release=args.days,
        margin_threshold=args.threshold,
    )

    print(json.dumps(result, indent=2))
