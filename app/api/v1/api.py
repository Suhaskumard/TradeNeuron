"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.models import Stock, Prediction
from app.schemas.stock import StockCreate, StockResponse

router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "traderneuron-api"}

@router.get("/stocks", response_model=List[StockResponse], tags=["stocks"])
async def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(Stock).all()
    return stocks

@router.post("/stocks", response_model=StockResponse, tags=["stocks"])
async def create_stock(stock_in: StockCreate, db: Session = Depends(get_db)):
    # Check if exists
    existing = db.query(Stock).filter(Stock.symbol == stock_in.symbol).first()
    if existing:
        raise HTTPException(status_code=400, detail="Stock already exists")
    
    stock = Stock(**stock_in.dict())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock
"""

