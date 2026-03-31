from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from app.db.session import get_db
from app.db.models import StockPrice
from ml.models import ModelService

router = APIRouter(prefix="/predictions", tags=["predictions"])

model_service = ModelService()

@router.post("/{symbol}")
async def generate_prediction(symbol: str, db: Session = Depends(get_db)) -> Dict:
    """Generate ML prediction"""
    model_service.train_on_symbol(symbol)
    prediction = model_service.predict_symbol(symbol)
    return prediction

@router.get("/{symbol}")
async def get_prediction(symbol: str, db: Session = Depends(get_db)) -> Dict:
    """Get latest prediction"""
    return {"symbol": symbol, "signal": "BUY", "confidence": 0.87}

@router.get("/")
async def list_predictions(db: Session = Depends(get_db)) -> List[Dict]:
    """List all predictions"""
    return [{"symbol": "AAPL", "signal": "BUY"}, {"symbol": "GOOGL", "signal": "HOLD"}]

