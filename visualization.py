import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, Any, List
import matplotlib.dates as mdates

def plot_price_trend(historical_data: Dict[str, Any], symbol: str) -> None:
    data = historical_data["Data"]["Data"]
    dates: List[datetime] = [datetime.fromtimestamp(entry["time"]) for entry in data]
    prices: List[float] = [entry["close"] for entry in data]

    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot the line
    ax.plot(dates, prices, linewidth=2, color='#2ecc71')
    
    # Fill the area under the line
    ax.fill_between(dates, prices, alpha=0.2, color='#2ecc71')
    
    # Customize the plot
    ax.set_title(f"{symbol} Price Trend", fontsize=16, pad=20)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Price (USD)", fontsize=12)
    
    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f"{symbol}_trend.png", dpi=300, bbox_inches='tight')
    plt.close()