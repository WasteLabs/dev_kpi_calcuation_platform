import pandas as pd

from src.osrm import Client


class TestClient:

    def test_london_coordinates(
            self,
            osrm_client: Client,
            london_coordinates: pd.DataFrame,
    ):
        response = osrm_client.route(london_coordinates).content
        assert response["code"] == "Ok"

    def test_parametrization(
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
        assert len(response_def_params) > len(response_custom_params)
