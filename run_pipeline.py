"""Main pipeline entrypoint: executes end-to-end data processing and modeling."""

import numpy as np
import pandas as pd
from src.config import PipelineConfig
from src.econometric_models import (
    HarmonicTrendModel,
    EventDrivenShockDetector,
    LongTermTrendExtrapolator
)
from src.visualizer import PublicationVisualizer


def run_synthetic_benchmark():
    """Generates synthetic test data matching 2011-2015 distribution to validate modeling core offline."""
    print(">>> Running econometric modeling suite on benchmark spatio-temporal series...")
    
    n_days = 1826  # 5 years
    t = np.arange(n_days)
    dates = pd.date_range(start="2011-01-01", periods=n_days)
    
    # Simulate Med SST: Base 18°C + 0.05°C/yr trend + 5.5°C seasonal cycle + AR(1) noise
    trend = 18.0 + (0.05 / 365.25) * t
    seasonal = 5.5 * np.sin(2 * np.pi * PipelineConfig.ANNUAL_FREQUENCY * t - 1.2)
    noise = np.random.normal(0, 0.4, n_days)
    sst_med = trend + seasonal + noise
    
    # 1. Harmonic Decomposition
    model = HarmonicTrendModel(frequency=PipelineConfig.ANNUAL_FREQUENCY).fit(sst_med)
    y_pred = model.predict(n_days)
    residuals = sst_med - y_pred
    acf = HarmonicTrendModel.compute_residual_autocorrelation(residuals, max_lags=180)
    
    print(f"[Harmonic Model] Alpha_0 (Intercept): {model.intercept_:.4f}")
    print(f"[Harmonic Model] Linear Trend Drift : {model.coefficients_[0] * 365.25:.4f} °C/year")
    print(f"[Harmonic Model] Residual Variance  : {np.var(residuals):.4f}")
    
    # 2. Event-Driven Differencing
    delta_sst = EventDrivenShockDetector.compute_daily_returns(pd.Series(sst_med, index=dates))
    shocks = EventDrivenShockDetector.identify_negative_shocks(delta_sst, threshold=-0.8)
    print(f"[Shock Detector] Identified {len(shocks)} abrupt structural drawdown events.")
    
    # 3. Horizon 2100 Projection
    mean_drift_5yr = 0.024  # Example drift over 5 years
    extrapolation = LongTermTrendExtrapolator.project_drift(
        mean_delta=mean_drift_5yr,
        sample_years=5,
        target_year=PipelineConfig.PROJECTION_TARGET_YEAR,
        base_year=PipelineConfig.BASE_YEAR
    )
    print(f"[Extrapolation] Projected cumulative shift by {extrapolation['target_year']}: "
          f"{extrapolation['projected_total_change']:.4f} m (Rate: {extrapolation['annual_rate'] * 1000:.2f} mm/year)")
    
    # 4. Generate Visualizations
    PublicationVisualizer.plot_harmonic_decomposition(sst_med, y_pred, residuals)
    PublicationVisualizer.plot_residual_acf(acf)
    PublicationVisualizer.plot_shock_differencing(dates, delta_sst, threshold=-0.8)
    print(">>> Econometric execution completed successfully.")


if __name__ == "__main__":
    run_synthetic_benchmark()