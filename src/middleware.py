import logging
from typing import Any

import awswrangler as wr
import boto3
import pandas as pd

from . import environment as env
from .models import ProcessingStatus


status_schema = ProcessingStatus()


def send_status_to_athena(status_record: pd.DataFrame):
    STATUS_WR_EXPORT_PARQUET_CONFIGS = {
        "path": f"s3://{env.AWS_S3_BUCKET}/{env.APP_ENV}/02_primary/status/",
        "boto3_session": boto3.Session(region_name=env.AWS_REGION),
        "index": False,
        "dataset": True,
        "sanitize_columns": True,
        "database": env.AWS_GLUE_DATABASE,
        "table": f"{env.APP_ENV}_status",
        "partition_cols": [status_schema.processing_id],
        "use_threads": True,
        "mode": "overwrite_partitions",
    }
    try:
        wr.s3.to_parquet(df=status_record, **STATUS_WR_EXPORT_PARQUET_CONFIGS)
        logging.info("Processing status is exported succesfully")
    except Exception as exc:
        msg = f"Processing status is failed to be exported: {exc}"
        logging.error(msg)
        raise RuntimeError(msg)


def execute_session_with_status_log(
        session: object,
        event: dict[str, Any],
        context: dict[str, Any],
):
    status_record = None
    try:
        session.run_lifecycle()
        status_record = ProcessingStatus.factory_status_record(
            processing_id=session.processing_id,
            status="successfull",
            error_description="",
        )
    except Exception as exc:
        status_record = ProcessingStatus.factory_status_record(
            processing_id=session.processing_id,
            status="failure",
            error_description=str(exc),
        )
        logging.error(f"EXCEPTION:\n{exc}\n")
        logging.error(f"EVENT:\n{event}\n")
        logging.error(f"CONTEXT:\n{context}\n")
    finally:
        send_status_to_athena(status_record=status_record)

    return status_record
