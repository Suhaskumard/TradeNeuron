"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True)
    name = Column(String(255))
    sector = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    prices = relationship("StockPrice", back_populates="stock")
    predictions = relationship("Prediction", back_populates="stock")

class StockPrice(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(DateTime(timezone=True), index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    stock = relationship("Stock", back_populates="prices")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(DateTime(timezone=True), index=True)
    model = Column(String(50))  # lstm, prophet, xgboost
    predicted_price = Column(Float)
    confidence = Column(Float)
    signal = Column(String(10))  # BUY, SELL, HOLD
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    stock = relationship("Stock", back_populates="predictions")

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    entry_date = Column(DateTime(timezone=True))
    exit_date = Column(DateTime(timezone=True), nullable=True)
    entry_price = Column(Float)
    exit_price = Column(Float)
    quantity = Column(Float)
    side = Column(String(4))  # LONG, SHORT
    pnl = Column(Float)
    status = Column(String(20), default="OPEN")  # OPEN, CLOSED
    created_at = Column(DateTime(timezone=True), server_default=func.now())
"""

