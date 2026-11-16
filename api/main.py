"""
DropOrCop - FastAPI Service
Phase 5 Backend Service
"""

from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(
    title="DropOrCop Resale Valuation API",
    description="Predicts sneaker resale prices and COP/DROP verdicts.",
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = Path("models/best_model.joblib")
model = None


@app.on_event("startup")
def load_trained_model():
    global model
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        print(f"Loaded model artifact from {MODEL_PATH}")
    else:
        print(f"Warning: {MODEL_PATH} not found.")


class PredictRequest(BaseModel):
    brand: str = Field(..., example="Yeezy")
    retail_price: float = Field(..., gt=0, example=220.0)
    shoe_size: float = Field(..., gt=0, example=10.5)
    days_since_release: int = Field(..., ge=0, example=45)
    threshold: Optional[float] = Field(0.15, example=0.15)


class PredictResponse(BaseModel):
    brand: str
    retail_price: float
    shoe_size: float
    days_since_release: int
    estimated_resale_price: float
    estimated_profit: float
    profit_margin_pct: float
    verdict: str


@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}


@app.get("/brands")
def get_supported_brands():
    return {
        "brands": ["Yeezy", "Off-White"],
        "default_retail": {"Yeezy": 220.0, "Off-White": 190.0},
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    global model
    if model is None:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
        else:
            raise HTTPException(status_code=503, detail="Model artifact is not available on server.")

    input_df = pd.DataFrame(
        [
            {
                "brand": request.brand,
                "retail_price": float(request.retail_price),
                "shoe_size": float(request.shoe_size),
                "days_since_release": int(request.days_since_release),
            }
        ]
    )

    pred_resale = round(float(model.predict(input_df)[0]), 2)
    retail = round(float(request.retail_price), 2)
    estimated_profit = round(pred_resale - retail, 2)
    profit_margin_pct = round((estimated_profit / retail) * 100, 2) if retail > 0 else 0.0

    verdict = "COP" if (estimated_profit / retail) >= request.threshold else "DROP"

    return PredictResponse(
        brand=request.brand,
        retail_price=retail,
        shoe_size=request.shoe_size,
        days_since_release=request.days_since_release,
        estimated_resale_price=pred_resale,
        estimated_profit=estimated_profit,
        profit_margin_pct=profit_margin_pct,
        verdict=verdict,
    )
