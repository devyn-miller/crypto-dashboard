import time
from typing import Dict, Any, Optional
from datetime import datetime

class Cache:
    def __init__(self, ttl_seconds: int = 300):  # 5 minutes default TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            if time.time() - self.cache[key]["timestamp"] < self.ttl:
                return self.cache[key]["data"]
            del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = {
            "data": value,
            "timestamp": time.time()
        }

def format_price(price: float) -> str:
    return f"${price:,.2f}"

def format_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")