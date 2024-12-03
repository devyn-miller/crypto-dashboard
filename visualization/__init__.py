from typing import Dict, Any
from .plotter import CryptoPlotter

def plot_price_trend(historical_data: Dict[str, Any], symbol: str) -> None:
    """Create and save a price trend plot."""
    try:
        plotter = CryptoPlotter(symbol, historical_data)
        plotter.plot_main_line()
        plotter.add_moving_average()
        plotter.add_annotations()
        plotter.format_axes()
        plotter.save()
    except Exception as e:
        print(f"Error creating plot for {symbol}: {str(e)}")
        raise