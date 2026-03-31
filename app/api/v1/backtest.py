from fastapi import APIRouter
from typing import Dict
from backtest.engine import BacktestEngine

router = APIRouter(prefix="/backtest", tags=["backtest"])

bt_engine = BacktestEngine()

@router.post("/{symbol}")
async def run_backtest(symbol: str) -> Dict:
    """Run backtest"""
    df = pd.DataFrame()  # Load from DB
    result = bt_engine.run(df, pd.Series())
    return result.__dict__

@router.get("/benchmark/{symbol}")
async def benchmark(symbol: str) -> Dict:
    df = pd.DataFrame()
    return bt_engine.benchmark(df)

