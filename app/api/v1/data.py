from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.db.session import get_db
from app.services.data_fetcher import fetch_and_save
from app.db.models import Stock

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/refresh/{symbol}")
async def refresh_data(symbol: str, db: Session = Depends(get_db)) -> Dict:
    """Refresh stock data"""
    try:
        result = fetch_and_save(symbol, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbols")
async def list_symbols(db: Session = Depends(get_db)) -> List[str]:
    """List available symbols"""
    symbols = db.query(Stock.symbol).all()
    return [s[0] for s in symbols]

@router.get("/prices/{symbol}")
async def get_prices(symbol: str, db: Session = Depends(get_db)):
    """Get recent prices"""
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Symbol not found")
    
    prices = db.query(StockPrice).filter(StockPrice.stock_id == stock.id).order_by(StockPrice.date.desc()).limit(100).all()
    return {"symbol": symbol, "prices": len(prices), "data": prices}

