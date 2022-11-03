import pandas as pd
import pandera as pa
import pytest


@pytest.fixture
def stops_to_order(stops_schema: object) -> pd.DataFrame:
    return pd.DataFrame({
        stops_schema.route_sequence: [2, 1, 0],
        "dummy_field": [0, 1, 2],
    })


@pytest.fixture
def expected_stops_order(stops_schema: object) -> pd.DataFrame:
    return pd.DataFrame({
        stops_schema.route_sequence: [0, 1, 2],
        "dummy_field": [2, 1, 0],
    })


@pytest.fixture
def correct_stops_schema() -> pd.DataFrame:
    return pd.DataFrame({
        "latitude": [0, 1, 2],
        "longitude": [0, 1, 2],
    })


def incorrect_stops_schema_1() -> pd.DataFrame:
    return pd.DataFrame({
        "latitude": ["a", "b", "c"],
        "longitude": [0, 1, 2],
    })


def incorrect_stops_schema_2() -> pd.DataFrame:
    return pd.DataFrame({})


@pytest.fixture
def pandera_stops_schema(stops_schema: object) -> pd.DataFrame:
    return stops_schema.factory_raw_user_stops_schema()


class TestStopsSchema:

    def test_order_stops(
            self,
            stops_schema: object,
            stops_to_order: pd.DataFrame,
            expected_stops_order: pd.DataFrame,
    ):
        assert stops_schema.order_stops(stops_to_order).equals(expected_stops_order)

    def test_factory_raw_user_stops_schema(
            self,
            stops_schema: object,
    ):
        assert isinstance(
            stops_schema.factory_raw_user_stops_schema(),
            pa.DataFrameSchema,
        )

    def test_succesfull_validation(
            self,
            pandera_stops_schema: pa.DataFrameSchema,
            london_coordinates: pd.DataFrame,
    ):
        pandera_stops_schema.validate(london_coordinates)

    @pytest.mark.parametrize(
        "incorrect_stops_schema",
        [
            incorrect_stops_schema_1(),
            incorrect_stops_schema_2(),
        ],
    )
    def test_incorrect_validations(
            self,
            pandera_stops_schema: pa.DataFrameSchema,
            incorrect_stops_schema: pd.DataFrame,
    ):
        try:
            pandera_stops_schema.validate(incorrect_stops_schema)
            raise AssertionError("Must fail due to incorrect schema")
        except pa.errors.SchemaError:
            assert True
