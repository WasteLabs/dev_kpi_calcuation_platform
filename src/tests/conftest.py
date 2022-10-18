import pandas as pd
import pytest


@pytest.fixture
def host() -> str:
    return "http://router.project-osrm.org/"


@pytest.fixture
def london_coordinates() -> pd.DataFrame:
    return pd.DataFrame([
        {'latitude': 51.48288180847117, 'longitude': -0.0588430532506331},
        {'latitude': 51.47482413883279, 'longitude': -0.0291032786878821},
        {'latitude': 51.4718502496285, 'longitude': -0.0320751884543755},
        {'latitude': 51.47088782010107, 'longitude': -0.0345428331590431},
    ])
