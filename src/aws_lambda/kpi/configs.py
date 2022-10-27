import boto3

from ...models import StopsSchema
from ... import environment as env

stops_schema = StopsSchema()


STOPS_WR_EXPORT_PARQUET_CONFIGS = {
    "path": "s3://dev-data-temp/dev_kpi_calculation_platform/dev/02_intermediate/stops/",
    "boto3_session": boto3.Session(region_name=env.AWS_REGION),
    "index": False,
    "dataset": True,
    "sanitize_columns": True,
    "database": "kpi_calculation_platform",
    "table": f"{env.APP_ENV}_stops",
    "partition_cols": [stops_schema.col_processing_id],
    "use_threads": True,
    "mode": "overwrite_partitions",
}


KPI_WR_EXPORT_PARQUET_CONFIGS = {
    "path": "s3://dev-data-temp/dev_kpi_calculation_platform/dev/02_intermediate/kpi/",
    "boto3_session": boto3.Session(region_name=env.AWS_REGION),
    "index": False,
    "dataset": True,
    "sanitize_columns": True,
    "database": "kpi_calculation_platform",
    "table": f"{env.APP_ENV}_kpi",
    "partition_cols": [stops_schema.col_processing_id],
    "use_threads": True,
    "mode": "overwrite_partitions",
}
