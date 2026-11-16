from fastapi import FastAPI
from typing import Any

app = FastAPI(title="DropOrCop API")

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to DropOrCop API!"}


# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "DropOrCop API",
        "model_status": "not_connected"
    }


# Brands endpoint
@app.get("/brands")
def get_brands():
    brands = ["Nike", "Adidas", "Puma", "New Balance"]

    return {
        "brands": brands,
        "total": len(brands)
    }


# Prediction endpoint
@app.post("/predict")
def predict(payload: dict[str, Any]):

    if not payload:
        return {
            "status": "error",
            "message": "Product information is required"
        }

    return {
        "status": "pending",
        "message": "ML model integration is pending",
        "received_fields": list(payload.keys())
    }