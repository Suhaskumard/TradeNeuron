from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime
from app.core.config import settings
from ml.ensemble import TradingEnsemble
from rl.agent import RLAgent

@dataclass
class Signal:
    symbol: str
    signal: str
    confidence: float
    price: float
    timestamp: datetime = None

class StrategyEngine:
    def __init__(self):
        self.ml_model = TradingEnsemble()
        self.rl_model = None
        self.risk_manager = RiskManager()
    
    def generate_signals(self, data: Dict[str, pd.DataFrame]) -> List[Signal]:
        """Generate trading signals"""
        signals = []
        
        for symbol, df in data.items():
            # ML prediction
            ml_pred = self.ml_model.predict(df)
            
            # RL prediction (if trained)
            rl_signal = "HOLD"
            if self.rl_model:
                obs = self._get_obs(df)
                rl_signal = self.rl_model.predict(obs)
            
            # Combine
            final_signal = self._combine_signals(ml_pred['signal'], rl_signal, ml_pred['confidence'])
            
            # Risk check
            if self.risk_manager.approve_trade(final_signal, ml_pred['price']):
                signals.append(Signal(
                    symbol=symbol,
                    signal=final_signal,
                    confidence=ml_pred['confidence'],
                    price=ml_pred['predicted_price']
                ))
        
        return signals
    
    def _combine_signals(self, ml_signal: str, rl_signal: str, confidence: float) -> str:
        """Combine ML + RL"""
        if ml_signal == rl_signal:
            return ml_signal
        return "HOLD" if confidence < 0.7 else ml_signal
    
    def _get_obs(self, df):
        # Extract state for RL
        return np.zeros(8)  # Placeholder

class RiskManager:
    def __init__(self):
        self.max_risk_per_trade = settings.RISK_PER_TRADE
        self.max_positions = 5
        self.current_positions = {}
    
    def approve_trade(self, signal: str, price: float) -> bool:
        """Risk checks"""
        # Position sizing
        position_size = settings.INITIAL_CAPITAL * self.max_risk_per_trade
        
        # Portfolio limits
        if len(self.current_positions) >= self.max_positions:
            return False
        
        # Stop loss check
        return True  # Simplified

