import pytest

from src.osrm.drivers.models import RouteParameters


@pytest.fixture
def route_params() -> RouteParameters:
    return RouteParameters()


@pytest.fixture
def expected_url() -> RouteParameters:
    return "?overview=full&steps=true&alternatives=false&geometries=geojson&annotations=true&continue_straight=true"


class TestRouteParameters:

    def test_factory(self, route_params: RouteParameters):
        assert True

    def test_url_params_factory(
            self,
            route_params: RouteParameters,
            expected_url: str,
    ):
        assert route_params.url_parameters() == expected_url
