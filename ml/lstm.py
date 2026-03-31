"""
import tensorflow as tf
import numpy as np
from typing import Tuple
from sklearn.preprocessing import MinMaxScaler

class LSTMPredictor:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        
    def create_sequences(self, data: np.ndarray, seq_length: int = 60) -> Tuple[np.ndarray, np.ndarray]:
        X, y = [], []
        for i in range(seq_length, len(data)):
            X.append(data[i-seq_length:i])
            y.append(data[i])
        return np.array(X), np.array(y)
    
    def train(self, close_prices: pd.Series, epochs: int = 50):
        # Prepare data
        scaled_data = self.scaler.fit_transform(close_prices.values.reshape(-1, 1))
        X, y = self.create_sequences(scaled_data)
        
        # Model
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
            tf.keras.layers.LSTM(50),
            tf.keras.layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=epochs, batch_size=32, verbose=0)
        
        self.model = model
    
    def predict(self, close_prices: pd.Series, n_future: int = 1) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not trained")
        
        scaled_data = self.scaler.transform(close_prices.values.reshape(-1, 1))
        X = scaled_data[-60:].reshape(1, -1, 1)
        pred = self.model.predict(X, verbose=0)
        pred = self.scaler.inverse_transform(pred)[0][0]
        return pred
"""

