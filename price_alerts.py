from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Alert:
    high_threshold: float
    low_threshold: float
    last_triggered: Optional[datetime] = None

class PriceAlert:
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}

    def set_alert(self, symbol: str, high_threshold: float, low_threshold: float) -> None:
        self.alerts[symbol.upper()] = Alert(high_threshold, low_threshold)

    def remove_alert(self, symbol: str) -> bool:
        return bool(self.alerts.pop(symbol.upper(), None))

    def check_alerts(self, current_prices: Dict[str, Dict[str, float]]) -> List[Tuple[str, float, str]]:
        triggered = []
        current_time = datetime.now()

        for symbol, alert in self.alerts.items():
            if symbol not in current_prices:
                continue

            price = current_prices[symbol]["USD"]
            
            # Only trigger if we haven't triggered recently (within last hour)
            if (not alert.last_triggered or 
                (current_time - alert.last_triggered).total_seconds() > 3600):
                
                if price >= alert.high_threshold:
                    triggered.append((symbol, price, "above"))
                    alert.last_triggered = current_time
                elif price <= alert.low_threshold:
                    triggered.append((symbol, price, "below"))
                    alert.last_triggered = current_time

        return triggered

    def get_alerts(self) -> Dict[str, Dict[str, float]]:
        return {
            symbol: {
                "high": alert.high_threshold,
                "low": alert.low_threshold
            }
            for symbol, alert in self.alerts.items()
        }