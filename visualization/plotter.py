import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, Any, List, Optional
import matplotlib.dates as mdates
from .utils import (
    validate_data, 
    calculate_moving_average, 
    find_significant_points, 
    format_date_axis
)
from .style import STYLE_CONFIG, apply_style

class CryptoPlotter:
    def __init__(self, symbol: str, historical_data: Dict[str, Any]):
        if "Data" not in historical_data or "Data" not in historical_data["Data"]:
            raise ValueError(f"Invalid data structure for {symbol}")
            
        self.symbol = symbol
        self.data = validate_data(historical_data["Data"]["Data"])
        self.dates = [datetime.fromtimestamp(entry["time"]) for entry in self.data]
        self.prices = [entry["close"] for entry in self.data]
        
        self.fig, self.ax = plt.subplots(**STYLE_CONFIG['figure'])
        apply_style(self.ax)
        
    def plot_main_line(self) -> None:
        """Plot the main price line."""
        self.ax.plot(
            self.dates, 
            self.prices, 
            **STYLE_CONFIG['line']
        )
        self.ax.fill_between(
            self.dates, 
            self.prices, 
            **STYLE_CONFIG['fill']
        )
        
    def add_moving_average(self, window: int = 7) -> None:
        """Add moving average line to the plot."""
        ma = calculate_moving_average(self.prices, window)
        self.ax.plot(
            self.dates, 
            ma, 
            **STYLE_CONFIG['ma_line'],
            label=f'{window}-day Moving Average'
        )
        self.ax.legend()
        
    def add_annotations(self) -> None:
        """Add annotations for significant price points."""
        significant_points = find_significant_points(self.prices)
        
        for idx, price in significant_points:
            self.ax.annotate(
                f'${price:,.2f}',
                xy=(self.dates[idx], price),
                xytext=(10, 10),
                textcoords='offset points',
                **STYLE_CONFIG['annotation']
            )
            
    def format_axes(self) -> None:
        """Format the axes for better readability."""
        date_format = format_date_axis(len(self.dates))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        plt.xticks(rotation=45)
        
        self.ax.set_title(
            f"{self.symbol} Price Trend", 
            fontsize=16, 
            pad=20, 
            fontweight='bold'
        )
        
    def save(self, filename: Optional[str] = None) -> None:
        """Save the plot to a file."""
        if filename is None:
            filename = f"{self.symbol}_trend.png"
            
        plt.tight_layout()
        plt.savefig(filename, dpi=STYLE_CONFIG['figure']['dpi'], bbox_inches='tight')
        plt.close()