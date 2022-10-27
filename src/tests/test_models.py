import pandas as pd
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


class TestStopsSchema:

    def test_order_stops(
            self,
            stops_schema: object,
            stops_to_order: pd.DataFrame,
            expected_stops_order: pd.DataFrame,
    ):
        assert stops_schema.order_stops(stops_to_order).equals(expected_stops_order)
