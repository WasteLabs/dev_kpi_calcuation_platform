import pandas as pd
import pytest

from src.osrm.driver import QueryDriver


@pytest.fixture
def route_query_driver(host: str) -> QueryDriver:
    return QueryDriver(host=host, service="route")


@pytest.fixture
def df_coordinates() -> pd.DataFrame:
    return pd.DataFrame({
        "latitude": [0, 1, 2],
        "longitude": [0, 1, 2],
    })


@pytest.fixture
def expected_query() -> str:
    return (
        "http://router.project-osrm.org//route/v1/driving/0,0;1,1;2,2?"
        "overview=full&steps=true&alternatives=false"
        "&geometries=geojson&annotations=true&continue_straight=true"
    )


@pytest.fixture
def malformed_url() -> pd.DataFrame:
    return "dummy_text"


class TestRouteQueryDriver:

    def test_factory_missing_service_1(self):
        try:
            QueryDriver(host="dummy_host", service="dummy_driver")
            raise AssertionError("Must fail due to incorrect service paramter")
        except RuntimeError:
            assert True

    def test_factory_missing_service_2(self):
        try:
            QueryDriver(host="dummy_host", service=0)
            raise AssertionError("Must fail due to incorrect service paramter")
        except RuntimeError:
            assert True

    def test_preprocess_query(
            self,
            route_query_driver: QueryDriver,
            df_coordinates: pd.DataFrame,
            expected_query: str,
    ):
        preprocessed_query = route_query_driver.preprocess_query(df_coordinates)
        assert preprocessed_query == expected_query

    def test_route_query(
            self,
            route_query_driver: QueryDriver,
            london_coordinates: pd.DataFrame,
    ):
        query = route_query_driver.preprocess_query(london_coordinates)
        result = route_query_driver.query(query)
        assert result["code"] == "Ok"

    def test_malformed_url_query(
            self,
            route_query_driver: QueryDriver,
            malformed_url: str,
    ):
        try:
            route_query_driver.query(malformed_url)
        except RuntimeError as exc:
            assert isinstance(exc, Exception)
