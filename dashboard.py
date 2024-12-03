import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

from api_client import (
    get_current_price, 
    get_historical_data, 
    get_global_stats,
    get_top_gainers_and_losers,
    get_trending_cryptos
)
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
        - Right panel displays current prices and market stats
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

    # Top Gainers and Losers
    st.subheader("Top Gainers and Losers (24h)")
    try:
        gainers_losers = get_top_gainers_and_losers(limit=5)
        if gainers_losers:
            col_gain, col_loss = st.columns(2)
            
            with col_gain:
                st.markdown("### 🚀 Top Gainers")
                for coin in gainers_losers['gainers']:
                    change = coin['RAW']['USD']['CHANGEPCT24HOUR']
                    price = coin['RAW']['USD']['PRICE']
                    st.metric(
                        label=coin['CoinInfo']['Name'],
                        value=f"{format_price(price, prefix='$')}",
                        delta=f"{change:.2f}%"
                    )
            
            with col_loss:
                st.markdown("### 📉 Top Losers")
                for coin in gainers_losers['losers']:
                    change = coin['RAW']['USD']['CHANGEPCT24HOUR']
                    price = coin['RAW']['USD']['PRICE']
                    st.metric(
                        label=coin['CoinInfo']['Name'],
                        value=f"{format_price(price, prefix='$')}",
                        delta=f"{change:.2f}%"
                    )
    except Exception as e:
        st.error(f"Error fetching top gainers and losers: {str(e)}")

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
    
    # Trending Cryptocurrencies
    st.subheader("Trending Cryptocurrencies")
    try:
        trending = get_trending_cryptos(limit=5)
        if trending:
            for coin in trending:
                price = coin['RAW']['USD']['PRICE']
                change = coin['RAW']['USD']['CHANGEPCT24HOUR']
                st.metric(
                    label=f"{coin['CoinInfo']['Name']} ({coin['CoinInfo']['FullName']})",
                    value=f"{format_price(price, prefix='$')}",
                    delta=f"{change:.2f}%"
                )
        else:
            st.warning("Trending data not available")
    except Exception as e:
        st.error(f"Error fetching trending cryptocurrencies: {str(e)}")
