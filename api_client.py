import requests
from typing import Dict, Any, Optional, List
from config import API_KEY, BASE_URL
from utils import Cache

cache = Cache()

class APIError(Exception):
    pass

def handle_api_request(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise APIError(f"API request failed: {str(e)}")

def get_current_price(symbols: str) -> Optional[Dict[str, float]]:
    cache_key = f"price_{symbols}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL}/price"
        params = {
            "fsym": symbols.upper(),
            "tsyms": "USD",
            "api_key": API_KEY
        }
        data = handle_api_request(url, params)
        if "USD" in data:
            cache.set(cache_key, data)
            return data
        raise APIError("Invalid response format")
    except APIError as e:
        print(f"Error fetching price for {symbols}: {str(e)}")
        return None

def get_historical_data(symbol: str, days: int = 7) -> Optional[Dict[str, Any]]:
    try:
        url = f"{BASE_URL}/v2/histoday"
        params = {
            "fsym": symbol.upper(),
            "tsym": "USD",
            "limit": days,
            "api_key": API_KEY
        }
        data = handle_api_request(url, params)
        if data.get("Response") == "Success":
            return data
        raise APIError("Invalid response format")
    except APIError as e:
        print(f"Error fetching historical data for {symbol}: {str(e)}")
        return None

def get_global_stats() -> Optional[Dict[str, Any]]:
    cache_key = "global_stats"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL}/global"
        params = {"api_key": API_KEY}
        data = handle_api_request(url, params)
        if "Response" in data:
            cache.set(cache_key, data)
            return data
        raise APIError("Invalid response format")
    except APIError as e:
        print(f"Error fetching global stats: {str(e)}")
        return None

def get_top_gainers_and_losers(limit: int = 10) -> Optional[Dict[str, List[Dict[str, Any]]]]:
    cache_key = "top_gainers_losers"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL}/top/totalvolfull"
        params = {
            "limit": limit * 2,  # Fetch extra to ensure we have enough after filtering
            "tsym": "USD",
            "api_key": API_KEY
        }
        data = handle_api_request(url, params)
        
        if "Data" in data:
            coins = data["Data"]
            # Sort by 24h change percentage
            sorted_coins = sorted(coins, key=lambda x: float(x.get("RAW", {}).get("USD", {}).get("CHANGEPCT24HOUR", 0)))
            
            result = {
                "gainers": sorted_coins[-limit:],
                "losers": sorted_coins[:limit]
            }
            cache.set(cache_key, result, ttl_seconds=300)  # Cache for 5 minutes
            return result
        raise APIError("Invalid response format")
    except APIError as e:
        print(f"Error fetching top gainers and losers: {str(e)}")
        return None

def get_trending_cryptos(limit: int = 10) -> Optional[List[Dict[str, Any]]]:
    cache_key = "trending_cryptos"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL}/top/totalvolfull"
        params = {
            "limit": limit,
            "tsym": "USD",
            "api_key": API_KEY
        }
        data = handle_api_request(url, params)
        
        if "Data" in data:
            trending = data["Data"]
            cache.set(cache_key, trending, ttl_seconds=300)  # Cache for 5 minutes
            return trending
        raise APIError("Invalid response format")
    except APIError as e:
        print(f"Error fetching trending cryptocurrencies: {str(e)}")
        return None