import time
from typing import Dict, Any, Optional
from datetime import datetime

class Cache:
    def __init__(self, default_ttl: int = 300):  # 5 minutes default TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            if time.time() - self.cache[key]["timestamp"] < self.cache[key]["ttl"]:
                return self.cache[key]["data"]
            del self.cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        self.cache[key] = {
            "data": value,
            "timestamp": time.time(),
            "ttl": ttl_seconds if ttl_seconds is not None else self.default_ttl
        }

def format_price(price: float, prefix: str = '') -> str:
    if price >= 1_000_000_000:  # Billions
        return f"{prefix}{price / 1_000_000_000:.2f}B"
    elif price >= 1_000_000:  # Millions
        return f"{prefix}{price / 1_000_000:.2f}M"
    elif price >= 1_000:  # Thousands
        return f"{prefix}{price / 1_000:.2f}K"
    else:
        return f"{prefix}{price:.2f}"

def format_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")