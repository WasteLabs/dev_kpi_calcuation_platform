import pandas as pd
import pytest


from src.models import StopsSchema
from src.aws_lambda.kpi.session import Session


stops = StopsSchema()


@pytest.fixture
def session(s3_sample_path: str):
    return Session(source_path=s3_sample_path)


@pytest.fixture
def coordinates_for_tsp(london_coordinates: pd.DataFrame):
    return london_coordinates.drop(columns=[stops.route_sequence])


@pytest.fixture
def depot_mismatch() -> pd.DataFrame:
    return pd.DataFrame({
        "latitude": [0, 1, 2, 3, 4],
        "longitude": [0, 1, 2, 3, 4],
    })


@pytest.fixture
def invalid_schema() -> pd.DataFrame:
    return pd.DataFrame({
        "latitude": [0, 1, 2, 3, 4],
    })


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

    def __check_stops_ordering(self, df: pd.DataFrame, route_sequence_col):
        route_sequences = df[route_sequence_col]
        route_sequence = (route_sequences - route_sequences.shift(1))[1:]
        assert (route_sequence > 0).all()

    def test_process_stops(
            self,
            session: Session,
            london_coordinates: pd.DataFrame,
            stops_schema: object,
    ):
        session.stops = london_coordinates
        session.extract_osrm_route_details()
        session.process_stops()
        assert "stops" in session.__dict__
        self.__check_schema(schema=stops_schema, df=session.stops)
        self.__check_stops_ordering(
            df=session.stops.copy(),
            route_sequence_col=stops_schema.route_sequence,
        )

    def test_tsp_solving(
            self,
            session: Session,
            coordinates_for_tsp: pd.DataFrame,
            stops_schema: object,
    ):
        assert stops_schema.route_sequence not in coordinates_for_tsp.columns
        session.stops = coordinates_for_tsp
        session.ensure_route_sequence_presence()
        session.extract_osrm_route_details()
        session.process_stops()
        assert "stops" in session.__dict__
        self.__check_schema(schema=stops_schema, df=session.stops)
        self.__check_stops_ordering(
            df=session.stops.copy(),
            route_sequence_col=stops_schema.route_sequence,
        )

    def test_compute_kpi(
            self,
            session: Session,
            london_coordinates: pd.DataFrame,
            kpi_schema: object,
            stops_schema: object,
    ):
        session.stops = london_coordinates
        session.extract_osrm_route_details()
        session.compute_kpi()
        assert "kpi" in session.__dict__
        self.__check_schema(schema=kpi_schema, df=session.kpi)
        self.__check_stops_ordering(
            df=session.stops.copy(),
            route_sequence_col=stops_schema.route_sequence,
        )

    def test_invalid_schema(
            self,
            session: Session,
            invalid_schema: pd.DataFrame,
    ):
        session.stops = invalid_schema
        try:
            session.validate_user_stops()
            raise AssertionError("Must fail due to missing longitude column")
        except RuntimeError:
            assert True

    def test_depot_point_mismatch(
            self,
            session: Session,
            depot_mismatch: pd.DataFrame,
    ):
        session.stops = depot_mismatch
        try:
            session.validate_user_stops()
            raise AssertionError("Must fail due to depot coordinates mismatch")
        except RuntimeError:
            assert True

    def test_run_lifecycle(self, s3_sample_path: str):
        session = Session(source_path=s3_sample_path)
        session.run_lifecycle()
