from typing import Dict
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from .lstm import LSTMPredictor
from .xgboost import XGBoostPredictor
from .features import create_features, prepare_data

class TradingEnsemble:
    def __init__(self):
        self.lstm = LSTMPredictor()
        self.xgb = XGBoostPredictor()
        self.meta_model = LinearRegression()
        
    def fit(self, df: pd.DataFrame):
        """Train all models"""
        feat_df = create_features(df)
        X, y, _ = prepare_data(feat_df)
        
        # Train LSTM (uses close prices only)
        self.lstm.train(df['close'])
        
        # Train XGBoost
        self.xgb.train(X, y)
        
        # Train meta model (placeholder)
        self.meta_model.fit(X[-100:], y[-100:])
        print("Ensemble trained successfully")
    
    def predict(self, df: pd.DataFrame) -> Dict:
        """Generate prediction and trading signal"""
        feat_df = create_features(df)
        X, _, feature_names = prepare_data(feat_df)
        
        # Base predictions
        current_price = df['close'].iloc[-1]
        lstm_price = self.lstm.predict(df['close'])
        xgb_price = self.xgb.predict(X[-1:])[0]
        
        # Ensemble prediction
        ensemble_price = 0.5 * lstm_price + 0.5 * xgb_price
        
        # Trading signal
        if ensemble_price > current_price * 1.005:
            signal = "BUY"
            confidence = min(0.95, 0.7 + abs((ensemble_price - current_price) / current_price))
        elif ensemble_price < current_price * 0.995:
            signal = "SELL"
            confidence = min(0.95, 0.7 + abs((current_price - ensemble_price) / current_price))
        else:
            signal = "HOLD"
            confidence = 0.6
        
        return {
            "predicted_price": float(ensemble_price),
            "current_price": float(current_price),
            "signal": signal,
            "confidence": float(confidence),
            "lstm_price": float(lstm_price),
            "xgb_price": float(xgb_price)
        }

