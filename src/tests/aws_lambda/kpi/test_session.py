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

    def __check_schema(self, schema: object, df: pd.DataFrame):
        for key in schema.__dict__.values():
            assert key in df.columns

    def test_process_stops(
            self,
            session: Session,
            london_coordinates: pd.DataFrame,
            stops_schema: object,
    ):
        session.stops = london_coordinates
        session.process_stops()
        assert "stops" in session.__dict__
        self.__check_schema(schema=stops_schema, df=session.stops)

    def test_compute_kpi(
            self,
            session: Session,
            london_coordinates: pd.DataFrame,
            kpi_schema: object,
    ):
        session.stops = london_coordinates
        session.compute_kpi()
        assert "kpi" in session.__dict__
        self.__check_schema(schema=kpi_schema, df=session.kpi)

    def test_entire(self, s3_sample_path: str):
        session = Session(source_path=s3_sample_path)
        session.read_stops()
        session.process_stops()
        session.compute_kpi()
        session.export_kpi()
        session.export_stops()
