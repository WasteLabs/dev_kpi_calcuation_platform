from typing import Any

import pandas as pd
import pytest
from shapely.geometry import LineString

from src.osrm.parsers.route import RouteParser


@pytest.fixture
def response_coordinates() -> dict[str, Any]:
    return {
        "routes": [{
            "geometry": {
                "coordinates": [
                    [0, 0],
                    [1, 1],
                    [2, 2],
                ],
            },
        }],
    }


@pytest.fixture
def expected_coordinates() -> list[list[int]]:
    return [
        [0, 0],
        [1, 1],
        [2, 2],
    ]


@pytest.fixture
def expected_df_coordinates(expected_coordinates) -> list[list[int]]:
    return pd.DataFrame(
        expected_coordinates,
        columns=["longitude", "latitude"],
    )


@pytest.fixture
def total_route_duration() -> dict[str, Any]:
    return {"routes": [{"duration": 121}]}


@pytest.fixture
def expected_total_duration_sec() -> int:
    return 121


@pytest.fixture
def expected_total_duration_hour() -> int:
    return 0.033611


@pytest.fixture
def total_route_distance() -> dict[str, Any]:
    return {"routes": [{"distance": 1000}]}


@pytest.fixture
def expected_route_distance() -> int:
    return 1000


@pytest.fixture
def expected_route_distance_km() -> int:
    return 1.0


@pytest.fixture
def response_legs_duration_and_distance() -> list[str, Any]:
    return {
        "routes": [{
            "legs": [
                {
                    "duration": 1,
                    "distance": 1,
                }, {
                    "duration": 1,
                    "distance": 1,
                }, {
                    "duration": 1,
                    "distance": 1,
                },
            ],
        }],
    }


@pytest.fixture
def expected_legs() -> list[str, Any]:
    return [
        {
            "duration": 1,
            "distance": 1,
        }, {
            "duration": 1,
            "distance": 1,
        }, {
            "duration": 1,
            "distance": 1,
        },
    ]


@pytest.fixture
def expected_duration_per_stop_seconds() -> list[int]:
    return [0, 1, 1, 1]


@pytest.fixture
def expected_distance_per_stop_meters() -> list[int]:
    return [0, 1, 1, 1]


@pytest.fixture
def expected_distance_per_stop_km() -> list[float]:
    return [0.0, 0.001, 0.001, 0.001]


@pytest.fixture
def expected_duration_per_stop_hours() -> list[float]:
    return [0.0, 0.000278, 0.000278, 0.000278]


class TestRouteParser:

    def test_coordinates_parse(
            self,
            response_coordinates: dict[str, Any],
            expected_coordinates: list[list[int]],
    ):
        parser = RouteParser(content=response_coordinates)
        assert parser.coordinates == expected_coordinates

    def test_coordinates_parse_df(
            self,
            response_coordinates: dict[str, Any],
            expected_df_coordinates: list[list[int]],
    ):
        parser = RouteParser(content=response_coordinates)
        assert isinstance(parser.df_coordinates, pd.DataFrame)
        assert parser.df_coordinates.equals(expected_df_coordinates)

    def test_parse_total_duration_sec(
            self,
            total_route_duration: dict[str, Any],
            expected_total_duration_sec: int,
    ):
        parser = RouteParser(content=total_route_duration)
        assert parser.total_duration_sec == expected_total_duration_sec

    def test_parse_total_duration_hour(
            self,
            total_route_duration: dict[str, Any],
            expected_total_duration_hour: int,
    ):
        parser = RouteParser(content=total_route_duration)
        assert parser.total_duration_hour == expected_total_duration_hour

    def test_linestring_coordinates_parse(
            self,
            response_coordinates: dict[str, Any],
            expected_df_coordinates: list[list[int]],
    ):
        parser = RouteParser(content=response_coordinates)
        assert isinstance(parser.linestring_coordinates, LineString)

    def test_total_distance_meter(
            self,
            total_route_distance: dict[str, Any],
            expected_route_distance: int,
    ):
        parser = RouteParser(content=total_route_distance)
        assert parser.total_distance_meters == expected_route_distance

    def test_total_distance_km(
            self,
            total_route_distance: dict[str, Any],
            expected_route_distance_km: int,
    ):
        parser = RouteParser(content=total_route_distance)
        assert parser.total_distance_km == expected_route_distance_km

    def test_malformed_key_sequence_1(
            self,
            response_coordinates: dict[str, Any],
            expected_coordinates: list[list[int]],
    ):
        try:
            RouteParser(content=response_coordinates)._get_key_seq_value(
                response_coordinates,
                key_sequence=["DUMMY_KEY"],
            )
        except RuntimeError:
            assert True

    def test_malformed_key_sequence_2(
            self,
            response_coordinates: dict[str, Any],
            expected_coordinates: list[list[int]],
    ):
        try:
            RouteParser(content=response_coordinates)._get_key_seq_value(
                response_coordinates,
                key_sequence=["routes", 1],
            )
        except RuntimeError:
            assert True

    def test_malformed_key_sequence_3(
            self,
            response_coordinates: dict[str, Any],
            expected_coordinates: list[list[int]],
    ):
        try:
            RouteParser(content=response_coordinates)._get_key_seq_value(
                response_coordinates,
                key_sequence=["routes", "dummy_reference"],
            )
        except RuntimeError:
            assert True

    def test_legs_extraction(
            self,
            response_legs_duration_and_distance: dict[str, Any],
            expected_legs: list[dict[str, int]],
    ):
        parser = RouteParser(content=response_legs_duration_and_distance)
        assert parser.legs == expected_legs

    def test_distance_per_stop_meters(
            self,
            response_legs_duration_and_distance: dict[str, Any],
            expected_distance_per_stop_meters: list[dict[str, int]],
    ):
        parser = RouteParser(content=response_legs_duration_and_distance)
        assert parser.distance_per_stop_meters == expected_distance_per_stop_meters

    def test_duration_per_stop_seconds(
            self,
            response_legs_duration_and_distance: dict[str, Any],
            expected_duration_per_stop_seconds: list[dict[str, int]],
    ):
        parser = RouteParser(content=response_legs_duration_and_distance)
        assert parser.duration_per_stop_seconds == expected_duration_per_stop_seconds

    def test_distance_per_stop_km(
            self,
            response_legs_duration_and_distance: dict[str, Any],
            expected_distance_per_stop_km: list[dict[str, int]],
    ):
        parser = RouteParser(content=response_legs_duration_and_distance)
        assert parser.distance_per_stop_km == expected_distance_per_stop_km

    def test_distance_per_stop_hours(
            self,
            response_legs_duration_and_distance: dict[str, Any],
            expected_duration_per_stop_hours: list[dict[str, int]],
    ):
        parser = RouteParser(content=response_legs_duration_and_distance)
        assert parser.duration_per_stop_hours == expected_duration_per_stop_hours
