"""Configuration module for Cloud Spatio-Temporal Econometrics Pipeline."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class RegionCoordinates:
    """Bounding box coordinates for target geographical regions."""
    lon_min: float
    lon_max: float
    lat_min: float
    lat_max: float


class PipelineConfig:
    """Global configuration settings for data extraction and modeling."""
    
    # GCP / BigQuery configurations
    GCP_PROJECT_ID: str = "alert-ground-261008"
    BQ_DATASET_TABLE: str = "bdo2020.bdo2020.2011_2015"
    
    # Region definitions
    AGULHAS_CURRENT = RegionCoordinates(lon_min=15.0, lon_max=70.0, lat_min=-50.0, lat_max=-30.0)
    EQUATORIAL_PACIFIC = RegionCoordinates(lon_min=180.0, lon_max=300.0, lat_min=-20.0, lat_max=20.0)
    JAPAN_TYPHOON_ZONE = RegionCoordinates(lon_min=120.0, lon_max=145.0, lat_min=20.0, lat_max=40.0)
    MEDITERRANEAN_SEA = RegionCoordinates(lon_min=0.0, lon_max=35.0, lat_min=30.0, lat_max=45.0)
    
    # Econometric Modeling
    ANNUAL_FREQUENCY: float = 1.0 / 365.25
    BASE_YEAR: int = 2011
    PROJECTION_TARGET_YEAR: int = 2100