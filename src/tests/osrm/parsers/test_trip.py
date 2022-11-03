from typing import Any

import pandas as pd
import pytest

from src.osrm.parsers.trip import TripParser


@pytest.fixture
def sample_waypoints() -> dict[str, Any]:
    return {
        "code": "Ok",
        "trips": [],
        "waypoints": [
            {
                'waypoint_index': 0,
                'trips_index': 0,
                'distance': 15.999561,
                'name': '',
                'location': [-0.058613, 51.482875],
            }, {
                'waypoint_index': 20,
                'trips_index': 0,
                'distance': 5.08482,
                'name': 'Florence Road',
                'location': [-0.029038, 51.474803],
            },
        ],
    }


@pytest.fixture
def expected_waypoints() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                'waypoint_index': 0,
                'trips_index': 0,
                'distance': 15.999561,
                'name': '',
                'location': [-0.058613, 51.482875],
            }, {
                'waypoint_index': 20,
                'trips_index': 0,
                'distance': 5.08482,
                'name': 'Florence Road',
                'location': [-0.029038, 51.474803],
            },
        ],
    )


@pytest.fixture
def expected_route_sequence() -> list[int]:
    return [0, 20]


class TestRouteParser:

    def test_waypoints(
            self,
            sample_waypoints: dict[str, Any],
            expected_waypoints: list[list[int]],
    ):
        parser = TripParser(content=sample_waypoints)
        assert isinstance(parser.waypoints, pd.DataFrame)
        assert parser.waypoints.equals(expected_waypoints)

    def test_route_sequence(
            self,
            sample_waypoints: dict[str, Any],
            expected_route_sequence: list[int],
    ):
        parser = TripParser(content=sample_waypoints)
        assert isinstance(parser.route_sequence, list)
        assert parser.route_sequence == expected_route_sequence
