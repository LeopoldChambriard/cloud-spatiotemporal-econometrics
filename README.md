# Cloud Spatio-Temporal Econometrics & Alternative Data Pipeline

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GCP BigQuery](https://img.shields.io/badge/Google_Cloud-BigQuery-orange.svg)](https://cloud.google.com/bigquery)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-econometrics-green.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A scalable quantitative data pipeline and econometric framework designed to ingest, process, and model a **50 GB multi-dimensional spatio-temporal satellite dataset** (2011–2015) hosted on Google Cloud Platform. 

The project applies structural time-series decomposition, spatial cross-correlation analysis, high-frequency shock differencing, and residual autocorrelation diagnostics to multi-variate physical ocean dynamics (Sea Surface Temperature & Sea Surface Height).

---

## Key Highlights & Methodological Architecture

### 1. Large-Scale Cloud Data Querying (GCP BigQuery & SQL)
- Executed high-throughput analytical SQL queries over 50 GB of unchronologically indexed spatio-temporal observations.
- Leveraged serverless aggregation functions (`CORR`, `MAX_BY`, `MIN_BY`, analytical partitions) to compute cross-sectional spatial statistics directly in-database, reducing memory footprint and network transfer latency.

### 2. Harmonic Time-Series Decomposition & Residual Diagnostics
Modeled long-term deterministic drift and seasonal periodicities using an OLS harmonic design matrix:
$$\text{SST}(t) = \alpha_0 + \alpha_1 t + \alpha_2 \sin(2\pi\omega t) + \alpha_3 \cos(2\pi\omega t), \quad \omega = \frac{1}{365.25}$$

- Formulated in-sample param estimation to isolate secular trends from solar radiative forcing.
- Computed the normalized **Residual Autocorrelation Function (ACF)**:
$$\hat{\rho}(k) = \frac{\sum_{t=1}^{T-k} (e_t - \bar{e})(e_{t+k} - \bar{e})}{\sum_{t=1}^T (e_t - \bar{e})^2}$$
to evaluate model adequacy and detect higher-order uncaptured cyclical components.

### 3. Event-Driven Differencing & Shock Isolation
- Implemented first-order time-series differencing ($\Delta y_t = y_t - y_{t-1}$) across targeted coordinates to detect non-linear structural shocks (e.g., rapid post-typhoon SST dropoffs caused by vertical water column mixing).

### 4. Teleconnection & Spatial Cross-Correlation Mapping
- Mapped regional Pearson correlation fields between Sea Surface Temperature (SST) and Sea Surface Height (SSH) across dynamic ocean current boundaries (e.g., Agulhas Return Current), capturing thermal expansion dynamics ($r > 0.80$).

---

## Repository Structure

```text
├── src/
│   ├── config.py             # Geographical boundaries and simulation parameters
│   ├── bigquery_client.py    # Production GCP BigQuery API wrapper and SQL engine
│   ├── econometric_models.py # Harmonic regression, differencing, and ACF diagnostics
│   └── visualizer.py         # Publication-grade time-series and spatial figures
├── run_pipeline.py           # CLI execution entrypoint and validation runner
├── requirements.txt          # Python dependencies
└── README.md