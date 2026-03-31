from typing import Dict
import pandas as pd
from sqlalchemy.orm import Session
from ml.ensemble import TradingEnsemble
from app.services.data_fetcher import DataFetcher
from app.db.session import SessionLocal

class ModelService:
    def __init__(self):
        self.ensemble = TradingEnsemble()
    
    def train_on_symbol(self, symbol: str):
        """Train models on symbol data"""
        with SessionLocal() as db:
            result = DataFetcher.save_prices(symbol, db)  # Ensure data exists
        print(f"Training on {symbol}")
        # Load data, train (placeholder for full training)
        self.ensemble.fit(pd.DataFrame())  # Will implement full logic
        return {"status": "trained", "symbol": symbol}
    
    def predict_symbol(self, symbol: str) -> Dict:
        """Get prediction for symbol"""
        # Load latest data
        df = pd.DataFrame()  # Placeholder
        prediction = self.ensemble.predict(df)
        return prediction

