"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.models import Stock

class StockBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    sector: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockResponse(StockBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2
"""

