import pandas as pd
import pytest


from src.aws_lambda.kpi.session import Session


@pytest.fixture
def session(s3_sample_path: str):
    return Session(source_path=s3_sample_path)


class TestSession:

    def test_init(self, s3_sample_path: str, s3_fname: str):
        session = Session(source_path=s3_sample_path)
        assert s3_sample_path == session.source_path
        assert s3_fname == session.filename

    def test_read_stops(self, session: Session):
        session.read_stops()
        assert "stops" in session.__dict__
        assert isinstance(session.stops, pd.DataFrame)

    def test_process_stops(
            self,
            session: Session,
            london_coordinates: pd.DataFrame,
            stops_schema: object,
    ):
        session.stops = london_coordinates
        session.process_stops()
        assert stops_schema.col_filename in session.stops
        assert stops_schema.col_processing_datetime in session.stops
        assert stops_schema.col_processing_id in session.stops

    def test_compute_kpi(
            self,
            session: Session,
            london_coordinates: pd.DataFrame,
            stops_schema: object,
    ):
        session.stops = london_coordinates
        session.compute_kpi()
        assert "kpi" in session.__dict__
        assert stops_schema.col_filename in session.kpi
        assert stops_schema.col_processing_datetime in session.kpi
        assert stops_schema.col_processing_id in session.kpi
