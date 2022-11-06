import awswrangler as wr
import pandas as pd

from ...models import StopsSchema


schema = StopsSchema()


def read_excel_file(path: str) -> pd.DataFrame:
    return wr.s3.read_excel(path=path)


def expand_name(stops: pd.DataFrame, fname: str) -> pd.DataFrame:
    stops[schema.col_filename] = fname
    return stops


def expand_processing_time(
        stops: pd.DataFrame,
        timestamp_id: str,
) -> pd.DataFrame:
    stops[schema.col_processing_datetime] = timestamp_id
    return stops


def expand_processing_id(stops: pd.DataFrame, processing_id: str) -> pd.DataFrame:
    stops[schema.col_processing_id] = processing_id
    return stops


def export_parquet_to_athena(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
    return wr.s3.to_parquet(df=df, *args, **kwargs)
