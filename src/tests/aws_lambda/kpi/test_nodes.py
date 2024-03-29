import pandas as pd
import pytest

from src.aws_lambda.kpi import nodes


@pytest.fixture
def generate_id_sample(
        london_coordinates: pd.DataFrame,
        stops_schema: object,
) -> str:
    london_coordinates[stops_schema.col_filename] = "1"
    london_coordinates[stops_schema.col_processing_datetime] = "2"
    return london_coordinates


@pytest.fixture
def timestamp_id() -> str:
    return "2022-05-12 09:00:00"


class TestNodes:

    def test_read_excel_file(self, s3_sample_path: str) -> pd.DataFrame:
        stops = nodes.read_excel_file(
            path=s3_sample_path,
        )
        assert isinstance(stops, pd.DataFrame)

    def test_expand_name(
            self,
            london_coordinates: pd.DataFrame,
            stops_schema: object,
            s3_fname: str,
    ) -> pd.DataFrame:
        stops = nodes.expand_name(
            stops=london_coordinates,
            fname=s3_fname,
        )
        assert stops[stops_schema.col_filename].unique()[0] == s3_fname

    def test_expand_processing_time(
            self,
            london_coordinates: pd.DataFrame,
            stops_schema: object,
            timestamp_id: str,
    ) -> pd.DataFrame:
        stops = nodes.expand_processing_time(
            stops=london_coordinates,
            timestamp_id=timestamp_id,
        )
        assert isinstance(stops, pd.DataFrame)
        assert stops_schema.col_processing_datetime in stops.columns
        pd.to_datetime(stops[stops_schema.col_processing_datetime])

    def test_generate_id(
            self,
            generate_id_sample: pd.DataFrame,
            stops_schema: object,
    ) -> pd.DataFrame:
        stops = nodes.expand_processing_id(stops=generate_id_sample, processing_id="dummy_id")
        assert stops_schema.col_processing_id in stops.columns
