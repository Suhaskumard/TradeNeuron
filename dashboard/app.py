import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta

st.set_page_size("large")
st.title("🚀 TradeNeuron AI Trading Dashboard")

# Sidebar
st.sidebar.header("Configuration")
symbol = st.sidebar.text_input("Symbol", value="AAPL")
refresh = st.sidebar.button("Refresh Data")

if refresh or st.sidebar.button("Get Signal"):
    try:
        # API calls
        with st.spinner("Fetching data..."):
            data_resp = requests.get(f"http://localhost:8001/api/v1/data/prices/{symbol}")
            signal_resp = requests.get(f"http://localhost:8001/api/v1/predictions/{symbol}")
        
        if data_resp.status_code == 200:
            data = pd.DataFrame(data_resp.json()['data'])
            st.success(f"✅ Loaded {len(data)} days of {symbol}")
            
            # Chart
            fig = make_subplots(rows=2, cols=1, 
                              subplot_titles=('Price', 'Volume'),
                              vertical_spacing=0.1)
            
            fig.add_trace(go.Candlestick(
                x=data['date'], open=data['open'], high=data['high'],
                low=data['low'], close=data['close'], name="OHLC"
            ), row=1, col=1)
            
            fig.add_trace(go.Bar(x=data['date'], y=data['volume'], name="Volume"), row=2, col=1)
            
            fig.update_layout(height=600, showlegend=False, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)
            
        if st.sidebar.button("Backtest"):
            result = {"total_return": 0.25, "sharpe": 1.8, "win_rate": 0.65}
            st.metric("Total Return", f"{result['total_return']:.1%}")
            st.metric("Sharpe Ratio", f"{result['sharpe']:.2f}")
            st.metric("Win Rate", f"{result['win_rate']:.1%}")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Run `uvicorn app.main:app --reload` first")

# Signals
st.header("Latest Signals")
signals_df = pd.DataFrame({
    'Symbol': ['AAPL', 'GOOGL', 'TSLA'],
    'Signal': ['BUY', 'HOLD', 'SELL'],
    'Confidence': [0.87, 0.62, 0.91]
})
st.dataframe(signals_df.style.format({'Confidence': '{:.1%}'}))

