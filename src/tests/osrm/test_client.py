import pandas as pd

from src.osrm import Client


class TestClient:

    def test_route_service(
            self,
            osrm_client: Client,
            london_coordinates: pd.DataFrame,
    ):
        response = osrm_client.route(london_coordinates).content
        assert response["code"] == "Ok"

    def test_trip_service(
            self,
            osrm_client: Client,
            london_coordinates: pd.DataFrame,
    ):
        response = osrm_client.trip(london_coordinates).content
        assert response["code"] == "Ok"

    def __assert_response_difference(self, default: str, parametrized: str):
        assert len(default) > len(parametrized)

    def test_route_service_parametrization(
            self,
            osrm_client: Client,
            london_coordinates: pd.DataFrame,
    ):
        response_def_params = str(osrm_client.route(london_coordinates).content)
        response_custom_params = str(
            osrm_client.route(
                london_coordinates,
                overview="false",
                steps="false",
                continue_straight="false",
                annotations="false",
            ).content,
        )
        self.__assert_response_difference(
            response_def_params,
            response_custom_params,
        )

    def test_trip_service_parametrization(
            self,
            osrm_client: Client,
            london_coordinates: pd.DataFrame,
    ):
        response_def_params = str(osrm_client.trip(X=london_coordinates).content)
        response_custom_params = str(
            osrm_client.trip(
                london_coordinates,
                overview="false",
                steps="false",
            ).content,
        )
        self.__assert_response_difference(
            response_def_params,
            response_custom_params,
        )
