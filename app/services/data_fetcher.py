import yfinance as yf
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.db.models import Stock, StockPrice
import logging

logger = logging.getLogger(__name__)

class DataFetcher:
    @staticmethod
    def get_or_create_stock(symbol: str, db: Session) -> Stock:
        """Get or create stock"""
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            stock = Stock(symbol=symbol, name=f"{symbol} Stock")
            db.add(stock)
            db.commit()
            db.refresh(stock)
            logger.info(f"Created stock {symbol}")
        return stock

    @staticmethod
    def fetch_stock_data(symbol: str, period: str = "2y") -> pd.DataFrame:
        """Fetch raw data from yfinance"""
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if data.empty:
            raise ValueError(f"No data for {symbol}")
        data.reset_index(inplace=True)
        return data

    @staticmethod
    def save_prices(symbol: str, db: Session):
        """Fetch and save prices for symbol"""
        # Get/create stock
        stock = DataFetcher.get_or_create_stock(symbol, db)
        
        # Fetch data
        df = DataFetcher.fetch_stock_data(symbol)
        
        saved_count = 0
        for _, row in df.iterrows():
            # Check duplicate
            existing = db.query(StockPrice).filter(
                StockPrice.stock_id == stock.id,
                func.date(StockPrice.date) == row['Date'].date()
            ).first()
            
            if not existing:
                price = StockPrice(
                    stock_id=stock.id,
                    date=row['Date'],
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=float(row['Volume'])
                )
                db.add(price)
                saved_count += 1
        
        db.commit()
        logger.info(f"Saved {saved_count} new prices for {symbol}")
        return {"status": "success", "symbol": symbol, "saved": saved_count, "total_fetched": len(df)}

def fetch_and_save(symbol: str, db: Session):
    """API endpoint function"""
    return DataFetcher.save_prices(symbol, db)

# Test script
if __name__ == "__main__":
    with SessionLocal() as db:
        result = fetch_and_save("AAPL", db)
        print(result)

