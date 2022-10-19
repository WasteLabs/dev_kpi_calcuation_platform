from datetime import datetime

import awswrangler as wr
import pandas as pd

from ...models import StopsSchema


schema = StopsSchema()


def read_excel_file(path: str) -> pd.DataFrame:
    return wr.s3.read_excel(path=path)


def expand_name(stops: pd.DataFrame, fname: str) -> pd.DataFrame:
    stops[schema.col_filename] = fname
    return stops


def expand_processing_time(stops: pd.DataFrame) -> pd.DataFrame:
    _datetime = datetime.now().strftime(schema.datetime_format)
    stops[schema.col_processing_datetime] = str(_datetime)
    return stops


def generate_id(stops: pd.DataFrame) -> pd.DataFrame:
    stops[schema.col_processing_id] = (
        stops[schema.col_processing_datetime].astype(str) + "__" +
        stops[schema.col_filename].astype(str)
    )
    return stops
