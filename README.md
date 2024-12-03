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

### 4. Top Gainers and Losers

- Display top 5 gaining cryptocurrencies in the last 24 hours
- Display top 5 losing cryptocurrencies in the last 24 hours
- Real-time percentage changes and current prices

### 5. Trending Cryptocurrencies

- Show top trending cryptocurrencies
- Display current prices and 24-hour changes
- Based on trading volume and market activity

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

4. `get_top_gainers_and_losers(limit: int)`

   - Fetches top gaining and losing cryptocurrencies
   - Endpoint: `/data/top/totalvolfull`

5. `get_trending_cryptos(limit: int)`

   - Retrieves trending cryptocurrencies based on volume
   - Endpoint: `/data/top/totalvolfull`

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
   - Monitor top gainers and losers
   - Track trending cryptocurrencies

## Project Structure

```ini
crypto-dashboard/
├── dashboard.py          # Main Streamlit application
├── api_client.py         # CryptoCompare API interface
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
