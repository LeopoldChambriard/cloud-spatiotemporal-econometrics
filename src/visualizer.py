"""Publication-ready visualizations using Cartopy and Matplotlib."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PublicationVisualizer:
    """Generates analytical charts for time series and geospatial fields."""

    @staticmethod
    def setup_style():
        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.size': 11,
            'axes.labelsize': 12,
            'axes.titlesize': 13,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'figure.titlesize': 14,
            'lines.linewidth': 1.8
        })

    @classmethod
    def plot_harmonic_decomposition(cls, y_observed: np.ndarray, y_fitted: np.ndarray, residuals: np.ndarray, save_path: str = None):
        cls.setup_style()
        fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
        
        t = np.arange(len(y_observed))
        axes[0].plot(t, y_observed, color='#1f77b4', alpha=0.5, label='Observed SST')
        axes[0].plot(t, y_fitted, color='#d62728', label='Harmonic Model (Trend + Seasonal)')
        axes[0].set_ylabel('SST (°C)')
        axes[0].set_title('Mediterranean Sea Surface Temperature: Harmonic Fit')
        axes[0].legend(loc='upper right')

        axes[1].plot(t, residuals, color='#2ca02c', alpha=0.7, label='Residuals')
        axes[1].axhline(0, color='black', linestyle='--', linewidth=1)
        axes[1].set_ylabel('Residual (°C)')
        axes[1].set_xlabel('Time (Days since Jan 1, 2011)')
        axes[1].legend(loc='upper right')

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    @classmethod
    def plot_residual_acf(cls, acf: np.ndarray, max_lags: int = 180, save_path: str = None):
        cls.setup_style()
        plt.figure(figsize=(10, 4))
        lags = np.arange(min(len(acf), max_lags))
        plt.stem(lags, acf[:len(lags)], linefmt='b-', markerfmt='bo', basefmt='r-')
        plt.axhline(0, color='black', linewidth=0.8)
        plt.axhline(1.96 / np.sqrt(len(acf)), color='grey', linestyle='--', linewidth=1)
        plt.axhline(-1.96 / np.sqrt(len(acf)), color='grey', linestyle='--', linewidth=1)
        plt.xlabel('Lag (Days)')
        plt.ylabel('Autocorrelation')
        plt.title('Residual Autocorrelation Function (ACF)')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    @classmethod
    def plot_shock_differencing(cls, time_index: pd.Series, diff_series: pd.Series, threshold: float = -0.4, save_path: str = None):
        cls.setup_style()
        plt.figure(figsize=(12, 4))
        plt.plot(time_index, diff_series, color='#34495e', lw=1.2, label='Daily Δ SST')
        plt.axhline(threshold, color='#e74c3c', linestyle='--', label=f'Shock Threshold ({threshold}°C)')
        plt.ylabel('Δ SST (°C/day)')
        plt.xlabel('Date')
        plt.title('Pacific Typhoon Zone: High-Frequency Thermal Shocks')
        plt.legend(loc='lower left')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()