import pandas as pd
import numpy as np
from typing import Dict, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BacktestResult:
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    trades: int
    win_rate: float

class BacktestEngine:
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.commission = 0.001  # 0.1%
        
    def run(self, df: pd.DataFrame, signals: pd.Series) -> BacktestResult:
        """Run backtest on signals"""
        positions = pd.DataFrame(index=df.index, data={'signal': signals, 'position': 0.0})
        
        # Generate positions from signals
        positions['position'] = 0
        positions.loc[signals == 'BUY', 'position'] = 1.0
        positions.loc[signals == 'SELL', 'position'] = -1.0
        
        # Calculate returns
        df['market_return'] = df['close'].pct_change()
        df['strategy_return'] = positions['position'].shift(1) * df['market_return']
        df['strategy_return'] -= self.commission * abs(positions['position'].diff())
        
        # Metrics
        total_return = (df['strategy_return'] + 1).prod() - 1
        sharpe = df['strategy_return'].mean() / df['strategy_return'].std() * np.sqrt(252)
        cumulative = (df['strategy_return'] + 1).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        trades = (positions['position'].diff() != 0).sum()
        winning_trades = (df['strategy_return'] > 0).sum()
        win_rate = winning_trades / trades if trades > 0 else 0
        
        return BacktestResult(
            total_return=total_return,
            sharpe_ratio=sharpe,
            max_drawdown=max_drawdown,
            trades=trades,
            win_rate=win_rate
        )
    
    def benchmark(self, df: pd.DataFrame) -> Dict:
        """Buy & hold benchmark"""
        buy_hold_return = df['close'].iloc[-1] / df['close'].iloc[0] - 1
        benchmark_sharpe = df['close'].pct_change().mean() / df['close'].pct_change().std() * np.sqrt(252)
        return {
            "buy_hold_return": buy_hold_return,
            "buy_hold_sharpe": benchmark_sharpe
        }

