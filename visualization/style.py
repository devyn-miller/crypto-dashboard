from typing import Dict, Any
import matplotlib.pyplot as plt

STYLE_CONFIG = {
    'figure': {
        'figsize': (12, 7),
        'dpi': 300,
        'facecolor': '#f8f9fa'
    },
    'grid': {
        'linestyle': '--',
        'alpha': 0.7,
        'color': '#dee2e6'
    },
    'line': {
        'width': 2,
        'color': '#2ecc71'
    },
    'fill': {
        'alpha': 0.2,
        'color': '#2ecc71'
    },
    'ma_line': {
        'color': '#e74c3c',
        'width': 1.5,
        'alpha': 0.8
    },
    'annotation': {
        'fontsize': 8,
        'bbox': dict(
            boxstyle='round,pad=0.5',
            fc='yellow',
            alpha=0.5
        ),
        'arrowprops': dict(
            arrowstyle='->',
            connectionstyle='arc3,rad=0.3'
        )
    }
}

def apply_style(ax: plt.Axes) -> None:
    """Apply consistent styling to the plot."""
    ax.set_facecolor('#ffffff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=10)
    
    # Style the grid
    ax.grid(True, **STYLE_CONFIG['grid'])
    
    # Style the labels
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Price (USD)', fontsize=12, fontweight='bold')