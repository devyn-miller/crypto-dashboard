# Cryptocurrency Dashboard

A real-time cryptocurrency tracking dashboard built with Python and Streamlit, utilizing the CryptoCompare API.

## Features

### 1. Real-Time Price Tracking

- Fetch and display current prices for multiple cryptocurrencies
- Support for major cryptocurrencies (BTC, ETH, XRP, DOGE, ADA)
- Automatic price updates

### 2. Interactive Price Charts

- Historical price trends visualization
- Multiple timeframe options (24h, 7d, 30d, 90d)
- Interactive Plotly charts with zoom and pan capabilities

### 3. Global Market Statistics

- Total cryptocurrency market capitalization
- 24-hour trading volume
- Real-time market updates

### 4. Price Alert System

- Set custom price thresholds for cryptocurrencies
- Automated monitoring of price movements
- Alert notifications when thresholds are crossed

### 5. Data Caching

- Efficient API usage with local caching
- Configurable cache duration
- Reduced API calls for better performance

## API Implementation

This project interfaces with the CryptoCompare API, implementing the following endpoints and functions:

1. `get_current_price(symbols: str)`

   - Fetches real-time cryptocurrency prices
   - Endpoint: `/data/price`

2. `get_historical_data(symbol: str, days: int)`

   - Retrieves historical price data
   - Endpoint: `/data/v2/histoday`

3. `get_global_stats()`

   - Gets global market statistics
   - Endpoint: `/data/global`

4. `set_alert(symbol: str, high_threshold: float, low_threshold: float)`

   - Sets price alerts for cryptocurrencies
   - Local implementation with real-time monitoring

5. `check_alerts(current_prices: Dict)`

   - Monitors and triggers price alerts
   - Automated threshold checking

6. `remove_alert(symbol: str)`

   - Manages price alert removal
   - Alert system maintenance

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/crypto-dashboard.git
cd crypto-dashboard
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set up your API key:

- Get a free API key from [CryptoCompare](https://min-api.cryptocompare.com/)

- Create a `.streamlit/secrets.toml` file:

```toml
CRYPTOCOMPARE_API_KEY = "your_api_key_here"
```

- Or set an environment variable:

```bash
export CRYPTOCOMPARE_API_KEY="your_api_key_here"
```

## Usage

1. Start the dashboard:

```bash
streamlit run dashboard.py
```

2. Access the dashboard in your browser:

   - Local: http://localhost:8501
   - Cloud: Your deployed URL

3. Using the Dashboard:

   - Select cryptocurrencies from the sidebar
   - Choose your preferred timeframe
   - View real-time prices and charts
   - Set up price alerts as needed

## Project Structure

```ini
crypto-dashboard/
├── dashboard.py          # Main Streamlit application
├── api_client.py         # CryptoCompare API interface
├── price_alerts.py       # Price alert system
├── utils.py             # Helper functions
├── config.py            # Configuration settings
├── requirements.txt     # Project dependencies
└── visualization/       # Visualization components
```

## Deployment

The dashboard can be deployed on:

1. Streamlit Cloud (Recommended)
2. Heroku
3. DigitalOcean
4. AWS Elastic Beanstalk
