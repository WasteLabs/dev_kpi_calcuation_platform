import pandas as pd
import pytest

from src.models import KpiSchema
from src.models import StopsSchema
from src.osrm import Client


@pytest.fixture
def host() -> str:
    return "http://router.project-osrm.org"


@pytest.fixture
def london_coordinates() -> pd.DataFrame:
    return pd.DataFrame([
        {
            'latitude': 51.48288180847117,
            'longitude': -0.0588430532506331,
            'route_sequence': 0,
        },
        {
            'latitude': 51.47482413883279,
            'longitude': -0.0291032786878821,
            'route_sequence': 2,
        },
        {
            'latitude': 51.4718502496285,
            'longitude': -0.0320751884543755,
            'route_sequence': 1,
        },
        {
            'latitude': 51.47088782010107,
            'longitude': -0.0345428331590431,
            'route_sequence': 3,
        },
    ])


@pytest.fixture
def osrm_client(host: str) -> Client:
    return Client(host=host, timeout=5)


@pytest.fixture
def stops_schema() -> StopsSchema:
    return StopsSchema()


@pytest.fixture
def kpi_schema() -> KpiSchema:
    return KpiSchema()
