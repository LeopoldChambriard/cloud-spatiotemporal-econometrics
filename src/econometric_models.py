"""Econometric and statistical modeling: harmonic regression, differencing, and ACF."""

from typing import Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class HarmonicTrendModel:
    """Decomposes time-series into a deterministic linear trend and Fourier seasonal components."""

    def __init__(self, frequency: float = 1.0 / 365.25):
        self.frequency = frequency
        self.model = LinearRegression()
        self.intercept_: float = 0.0
        self.coefficients_: np.ndarray = np.array([])

    def _build_design_matrix(self, t: np.ndarray) -> np.ndarray:
        """Constructs design matrix: [t, sin(2*pi*w*t), cos(2*pi*w*t)]."""
        return np.column_stack([
            t,
            np.sin(2.0 * np.pi * self.frequency * t),
            np.cos(2.0 * np.pi * self.frequency * t)
        ])

    def fit(self, y: np.ndarray) -> "HarmonicTrendModel":
        """Fits regression parameters alpha_0, alpha_1, alpha_2, alpha_3."""
        t = np.arange(len(y))
        X = self._build_design_matrix(t)
        self.model.fit(X, y)
        self.intercept_ = float(self.model.intercept_)
        self.coefficients_ = self.model.coef_
        return self

    def predict(self, n_steps: int) -> np.ndarray:
        """Generates in-sample or out-of-sample fitted values."""
        t = np.arange(n_steps)
        X = self._build_design_matrix(t)
        return self.model.predict(X)

    @staticmethod
    def compute_residual_autocorrelation(residuals: np.ndarray, max_lags: int = 365) -> np.ndarray:
        """Calculates normalized autocorrelation function (ACF) of residuals."""
        centered = residuals - np.mean(residuals)
        variance = np.var(residuals)
        if variance == 0:
            return np.zeros(max_lags)
        autocov = np.correlate(centered, centered, mode='full')
        mid = len(residuals) - 1
        acf = autocov[mid:mid + max_lags] / (variance * len(residuals))
        return acf


class EventDrivenShockDetector:
    """Detects high-frequency exogenous shocks using first-order time-series differencing."""

    @staticmethod
    def compute_daily_returns(series: pd.Series) -> pd.Series:
        """Computes daily first-difference: Delta y(t) = y(t) - y(t-1)."""
        return series.diff().fillna(0.0)

    @staticmethod
    def identify_negative_shocks(delta_series: pd.Series, threshold: float = -0.4) -> pd.Series:
        """Filters days with abrupt drawdowns below a specified volatility threshold."""
        return delta_series[delta_series < threshold]


class LongTermTrendExtrapolator:
    """Projects linear trends for multi-decadal horizon forecasting."""

    @staticmethod
    def project_drift(mean_delta: float, sample_years: int, target_year: int, base_year: int) -> Dict[str, float]:
        """Calculates annual rate and extrapolates value to horizon year."""
        annual_rate = mean_delta / sample_years
        delta_years = target_year - base_year
        projected_value = annual_rate * delta_years
        return {
            "annual_rate": annual_rate,
            "projected_total_change": projected_value,
            "target_year": target_year
        }