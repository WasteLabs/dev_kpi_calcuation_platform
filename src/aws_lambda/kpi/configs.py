import boto3

from ...models import StopsSchema
from ... import environment as env

stops_schema = StopsSchema()


STOPS_WR_EXPORT_PARQUET_CONFIGS = {
    "path": f"s3://{env.AWS_S3_BUCKET}/{env.APP_ENV}/02_primary/stops/",
    "boto3_session": boto3.Session(region_name=env.AWS_REGION),
    "index": False,
    "dataset": True,
    "sanitize_columns": True,
    "database": env.AWS_GLUE_DATABASE,
    "table": f"{env.APP_ENV}_stops",
    "partition_cols": [stops_schema.col_processing_id],
    "use_threads": True,
    "mode": "overwrite_partitions",
}


KPI_WR_EXPORT_PARQUET_CONFIGS = {
    "path": f"s3://{env.AWS_S3_BUCKET}/{env.APP_ENV}/02_primary/kpi/",
    "boto3_session": boto3.Session(region_name=env.AWS_REGION),
    "index": False,
    "dataset": True,
    "sanitize_columns": True,
    "database": env.AWS_GLUE_DATABASE,
    "table": f"{env.APP_ENV}_kpi",
    "partition_cols": [stops_schema.col_processing_id],
    "use_threads": True,
    "mode": "overwrite_partitions",
}
