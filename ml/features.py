import pandas as pd
import numpy as np

def rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """Manual RSI calculation"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """Manual MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    return macd_line, signal_line

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Complete feature engineering"""
    df = df.copy()
    
    # Basic returns
    df['returns'] = df['close'].pct_change()
    df['volatility'] = df['returns'].rolling(20).std()
    
    # Price ratios
    df['high_low'] = df['high'] / df['low']
    df['close_open'] = df['close'] / df['open']
    
    # Lags
    for lag in [1, 2, 3, 5]:
        df[f'close_lag_{lag}'] = df['close'].shift(lag)
        df[f'returns_lag_{lag}'] = df['returns'].shift(lag)
    
    # Rolling stats
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df['bb_position'] = (df['close'] - df['ma20']) / df['close'].rolling(20).std()
    
    # Manual TA indicators
    df['rsi'] = rsi(df['close'])
    df['macd'], df['macd_signal'] = macd(df['close'])
    
    # Volume features
    df['volume_ma'] = df['volume'].rolling(10).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma']
    
    # Target
    df['target'] = df['close'].shift(-1)
    
    df.dropna(inplace=True)
    return df

def prepare_data(df: pd.DataFrame, target_col: str = 'target'):
    """Prepare for ML"""
    feature_cols = [col for col in df.columns 
                   if col not in ['date', 'open', 'high', 'low', 'close', 'volume', 'target']]
    X = df[feature_cols].values
    y = df[target_col].values
    return X, y, feature_cols

