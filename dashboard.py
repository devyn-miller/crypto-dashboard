import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

from api_client import get_current_price, get_historical_data, get_global_stats
from utils import format_price

# Page config
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Cryptocurrency Dashboard")

# Instructions button in the sidebar
st.sidebar.header("Instructions")
with st.sidebar.expander("How to use this dashboard"):
    st.write("""
    1. **Select Cryptocurrencies**: Choose one or more cryptocurrencies from the dropdown menu below
    2. **Choose Timeframe**: Select your preferred time period for the price trend chart
    3. **View Data**:
        - Left panel shows price trends over time
        - Right panel displays current prices and global market stats
    4. **Interact with Charts**:
        - Hover over charts to see detailed values
        - Use the zoom and pan tools to explore different time periods
        - Double-click to reset the view
    """)

# Sidebar settings
st.sidebar.header("Settings")
crypto_symbols = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    ["BTC", "ETH", "XRP", "DOGE", "ADA"],
    default=["BTC", "ETH"]
)

timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ["24h", "7d", "30d", "90d"],
    index=1
)

# Convert timeframe to days
timeframe_days = {
    "24h": 1,
    "7d": 7,
    "30d": 30,
    "90d": 90
}[timeframe]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Price Trends")
    
    # Create price trend chart
    fig = go.Figure()
    
    for symbol in crypto_symbols:
        try:
            historical_data = get_historical_data(symbol, timeframe_days)
            if historical_data and 'Data' in historical_data:
                df = pd.DataFrame(historical_data['Data']['Data'])
                df['time'] = pd.to_datetime(df['time'], unit='s')
                
                fig.add_trace(go.Scatter(
                    x=df['time'],
                    y=df['close'],
                    name=symbol,
                    mode='lines'
                ))
            else:
                st.warning(f"No historical data available for {symbol}")
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
    
    fig.update_layout(
        title=f"Price Trends ({timeframe})",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Current Prices")
    
    # Current prices
    for symbol in crypto_symbols:
        try:
            price_data = get_current_price(symbol)
            if price_data and 'USD' in price_data:
                st.metric(
                    label=symbol,
                    value=f"{format_price(price_data['USD'], prefix='$')}"
                )
            else:
                st.warning(f"No price data available for {symbol}")
        except Exception as e:
            st.error(f"Error fetching price for {symbol}: {str(e)}")
    
    # Global stats
    st.subheader("Global Market Stats")
    try:
        global_stats = get_global_stats()
        if global_stats and 'Data' in global_stats:
            data = global_stats['Data']
            st.metric("Total Market Cap", f"{format_price(data.get('total_mcap', 0), prefix='$')}")
            st.metric("24h Volume", f"{format_price(data.get('total_volume24h', 0), prefix='$')}")
        else:
            st.warning("Global market stats not available")
    except Exception as e:
        st.error(f"Error fetching global stats: {str(e)}")
