import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd
from typing import Tuple, Dict

class XGBoostPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        
    def train(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Train XGBoost model"""
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Validate
        y_pred = self.model.predict(X_val)
        mae = mean_absolute_error(y_val, y_pred)
        
        self.feature_names = [f'f{i}' for i in range(X.shape[1])]
        
        return {"mae": mae}
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not trained")
        return self.model.predict(X)
    
    def feature_importance(self) -> pd.DataFrame:
        if self.model is None:
            return pd.DataFrame()
        importance = self.model.feature_importances_
        return pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)

