"""
DropOrCop - FastAPI Service
Phase 5 Backend Service
Connects trained Random Forest ML model to REST endpoints for sneaker resale valuation.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd

MODEL_PATH = Path("models/best_model.joblib")
SUPPORTED_BRANDS = ["Yeezy", "Off-White"]
DEFAULT_RETAIL_PRICES = {"Yeezy": 220.0, "Off-White": 190.0}

model = None


def get_model():
    """Helper to lazily load the model if not loaded at startup."""
    global model
    if model is None:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
        else:
            raise HTTPException(
                status_code=503,
                detail=f"Model artifact '{MODEL_PATH}' is not available on server.",
            )
    return model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: load model at startup."""
    global model
    if MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
            print(f"[DropOrCop API] Loaded ML model artifact from {MODEL_PATH}")
        except Exception as exc:
            print(f"[DropOrCop API] Failed to load model artifact: {exc}")
    else:
        print(f"[DropOrCop API] Warning: Model artifact not found at {MODEL_PATH}")
    yield


app = FastAPI(
    title="DropOrCop Resale Valuation API",
    description="REST API predicting sneaker resale prices and COP/DROP verdicts using trained ML pipeline.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    brand: str = Field(..., description="Sneaker brand (e.g. 'Yeezy' or 'Off-White')", example="Yeezy")
    retail_price: float = Field(..., gt=0, description="Original retail price in USD", example=220.0)
    shoe_size: float = Field(..., gt=0, description="US shoe size", example=10.5)
    days_since_release: int = Field(..., ge=0, description="Days elapsed since official release", example=45)
    threshold: Optional[float] = Field(0.15, description="Profit margin threshold for COP verdict", example=0.15)


class PredictResponse(BaseModel):
    brand: str
    retail_price: float
    shoe_size: float
    days_since_release: int
    estimated_resale_price: float
    estimated_profit: float
    profit_margin_pct: float
    verdict: str


@app.get("/")
def home():
    """Home / Welcome endpoint."""
    return {
        "message": "Welcome to DropOrCop API!",
        "service": "DropOrCop Resale Valuation API",
        "version": "1.0.0",
        "docs_url": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint reporting server & model status."""
    is_loaded = model is not None or MODEL_PATH.exists()
    return {
        "status": "healthy",
        "service": "DropOrCop API",
        "model_loaded": is_loaded,
        "model_status": "connected" if is_loaded else "not_connected",
    }


@app.get("/brands")
def get_supported_brands():
    """Returns supported sneaker brands and typical retail pricing."""
    return {
        "brands": SUPPORTED_BRANDS,
        "total": len(SUPPORTED_BRANDS),
        "default_retail": DEFAULT_RETAIL_PRICES,
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Predicts secondary market resale price, profit margin, and COP/DROP verdict.
    """
    trained_model = get_model()

    # Normalization / validation of brand name
    matched_brand = None
    for b in SUPPORTED_BRANDS:
        if request.brand.strip().lower() == b.lower():
            matched_brand = b
            break

    if not matched_brand:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported brand '{request.brand}'. Supported brands are: {SUPPORTED_BRANDS}",
        )

    # Prepare DataFrame for scikit-learn pipeline inference
    input_df = pd.DataFrame(
        [
            {
                "brand": matched_brand,
                "retail_price": float(request.retail_price),
                "shoe_size": float(request.shoe_size),
                "days_since_release": int(request.days_since_release),
            }
        ]
    )

    pred_resale = round(float(trained_model.predict(input_df)[0]), 2)
    retail = round(float(request.retail_price), 2)
    estimated_profit = round(pred_resale - retail, 2)
    profit_margin_pct = round((estimated_profit / retail) * 100, 2) if retail > 0 else 0.0

    verdict = "COP" if (estimated_profit / retail) >= request.threshold else "DROP"

    return PredictResponse(
        brand=matched_brand,
        retail_price=retail,
        shoe_size=request.shoe_size,
        days_since_release=request.days_since_release,
        estimated_resale_price=pred_resale,
        estimated_profit=estimated_profit,
        profit_margin_pct=profit_margin_pct,
        verdict=verdict,
    )
