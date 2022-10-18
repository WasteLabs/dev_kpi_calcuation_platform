from typing import Any
import pandas as pd
import pytest

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
