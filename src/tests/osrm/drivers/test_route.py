import pandas as pd
import pytest

from src.osrm.drivers.route import RouteQueryDriver


@pytest.fixture
def query_driver(host: str) -> RouteQueryDriver:
    return RouteQueryDriver(host=host)


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


class TestRouteQueryDriver:

    def test_preprocess_query(
            self,
            query_driver: RouteQueryDriver,
            df_coordinates: pd.DataFrame,
            expected_query: str,
    ):
        preprocessed_query = query_driver.preprocess_query(df_coordinates)
        assert preprocessed_query == expected_query

    def test_query(
            self,
            query_driver: RouteQueryDriver,
            london_coordinates: pd.DataFrame,
    ):
        query = query_driver.preprocess_query(london_coordinates)
        result = query_driver.query(query)
        assert result["code"] == "Ok"
