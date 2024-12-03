from typing import List, Dict, Any, Tuple
from datetime import datetime
import pandas as pd
import numpy as np

def validate_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter out invalid entries from historical data."""
    return [
        entry for entry in data 
        if isinstance(entry.get("close"), (int, float)) and 
           isinstance(entry.get("time"), (int, float))
    ]

def calculate_moving_average(prices: List[float], window: int = 7) -> List[float]:
    """Calculate moving average for the given prices."""
    return list(pd.Series(prices).rolling(window=window).mean())

def find_significant_points(prices: List[float]) -> List[Tuple[int, float]]:
    """Find significant price points (peaks and troughs)."""
    significant_points = []
    for i in range(1, len(prices) - 1):
        # Check for local maxima and minima
        if (prices[i] > prices[i-1] and prices[i] > prices[i+1]) or \
           (prices[i] < prices[i-1] and prices[i] < prices[i+1]):
            significant_points.append((i, prices[i]))
    return significant_points

def format_date_axis(num_points: int) -> str:
    """Return appropriate date format based on number of data points."""
    if num_points > 50:
        return '%b %d'
    elif num_points > 365:
        return '%b %Y'
    return '%Y-%m-%d'