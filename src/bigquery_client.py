"""BigQuery client module for querying spatio-temporal satellite databases."""

import pandas as pd
from google.cloud import bigquery
from src.config import PipelineConfig, RegionCoordinates


class BigQueryDataExtractor:
    """Encapsulates SQL queries executed on Google Cloud BigQuery."""

    def __init__(self, project_id: str = PipelineConfig.GCP_PROJECT_ID):
        self.project_id = project_id
        self.client = bigquery.Client(project=self.project_id)
        self.table = PipelineConfig.BQ_DATASET_TABLE

    def execute_query(self, query: str) -> pd.DataFrame:
        """Executes a standard SQL query and returns a pandas DataFrame."""
        query_job = self.client.query(query)
        return query_job.to_dataframe()

    def get_spatial_correlation(self, region: RegionCoordinates) -> pd.DataFrame:
        """Computes point-wise spatial Pearson correlation between SST and SSH."""
        query = f"""
        SELECT
            lon,
            lat,
            CORR(sst, ssh) AS correlation
        FROM
            `{self.table}`
        WHERE
            lon BETWEEN {region.lon_min} AND {region.lon_max}
            AND lat BETWEEN {region.lat_min} AND {region.lat_max}
        GROUP BY
            lon, lat
        """
        return self.execute_query(query)

    def get_regional_daily_aggregate(self, region: RegionCoordinates) -> pd.DataFrame:
        """Extracts chronological daily mean and standard deviation for SST."""
        query = f"""
        SELECT
            time,
            AVG(sst) AS mean_sst,
            STDDEV(sst) AS std_sst
        FROM
            `{self.table}`
        WHERE
            lon BETWEEN {region.lon_min} AND {region.lon_max}
            AND lat BETWEEN {region.lat_min} AND {region.lat_max}
        GROUP BY
            time
        ORDER BY
            time ASC
        """
        return self.execute_query(query)

    def get_global_ssh_drift(self) -> pd.DataFrame:
        """Calculates total sea level drift by point between 2011 and 2015."""
        query = f"""
        SELECT
            lon,
            lat,
            MAX_BY(ssh, time) - MIN_BY(ssh, time) AS ssh_difference
        FROM
            `{self.table}`
        GROUP BY
            lon, lat
        """
        return self.execute_query(query)