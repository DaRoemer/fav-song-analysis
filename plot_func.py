"""
plot_func.py

This script contains helper functions for plotting and statistical analysis of Spotify liked songs data.
"""

import numpy as np
import pandas as pd
import seaborn as sns

def bootstrap_ci(data, n_bootstrap=1000, ci=95):
    """
    Compute bootstrap confidence interval for the mean of the data.

    Parameters:
    data (array-like): The data to compute the confidence interval for.
    n_bootstrap (int): The number of bootstrap samples to draw. Default is 1000.
    ci (float): The confidence interval percentage. Default is 95.

    Returns:
    tuple: Lower and upper bounds of the confidence interval.
    """
    boot_means = np.array([np.mean(np.random.choice(data, size=len(data), replace=True)) for _ in range(n_bootstrap)])
    lower = np.percentile(boot_means, (100 - ci) / 2)
    upper = np.percentile(boot_means, 100 - (100 - ci) / 2)
    return lower, upper

def add_middle_text(start, end, text, color, ax, yscale=0.95):
    """
    Add text in the middle of a plot.

    Parameters:
    start (datetime-like): The start date.
    end (datetime-like): The end date.
    text (str): The text to add.
    color (str): The color of the text.
    ax (matplotlib.axes.Axes): The axes to add the text to.
    yscale (float): The vertical position of the text relative to the y-axis limits. Default is 0.95.
    """
    mid_date = start + (end - start) / 2
    ax.text(mid_date, 
            ax.get_ylim()[1] * yscale, 
            text, 
            horizontalalignment='center', 
            verticalalignment='top', 
            fontsize=12, 
            color=color)

def ema(track_infos, col, ax, span=10):
    """
    Calculate and plot the Exponential Moving Average (EMA) of a given column in the track information.

    Parameters:
    track_infos (pd.DataFrame): DataFrame containing track information.
    col (str): The column to calculate the EMA for.
    ax (matplotlib.axes.Axes): The axes to plot the EMA on.
    span (int): The span for the EMA calculation. Default is 10.
    """
    EMA = pd.DataFrame()
    EMA['added_at'] = track_infos['added_at']
    EMA['EMA'] = track_infos[col].ewm(span=span).mean()
    EMA['EMA_std'] = track_infos[col].ewm(span=span).std()
    EMA['EMA_lower'], EMA['EMA_upper'] = bootstrap_ci(EMA['EMA'], n_bootstrap=1000, ci=95)
    
    sns.lineplot(data=EMA,
                 x='added_at', 
                 y='EMA', 
                 color='red', 
                 label='Exponential Moving Average', 
                 legend=False,
                 ax=ax)
    
    ax.fill_between(EMA['added_at'], 
                    EMA['EMA'] - EMA['EMA_std'], 
                    EMA['EMA'] + EMA['EMA_std'], 
                    color='red', alpha=0.2, 
                    label='EMA 95% CI')