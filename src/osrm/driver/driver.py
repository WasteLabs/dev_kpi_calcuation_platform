import logging
import requests
from typing import Any

import pandas as pd

from ..models import Schema
from . import mappings

schema = Schema()


class QueryDriver(object):

    def __init__(self, host: str, service: str, timeout: int = 5):
        self.__service_profile = self.__get_osrm_service_mapping(
            mapping=mappings.SERVICES_PROFILES,
            service=service,
        )
        self.__osrm_params = self.__get_osrm_service_mapping(
            mapping=mappings.PARAMETERS,
            service=service,
        )
        self.__host = host
        self.__timeout = timeout

    def __pack_url(self, service_profile: str, coordinates: str, params: str) -> str:
        return f"{self.host}/{service_profile}/{coordinates}{params}"

    def __lat_lon_df_to_url_string(self, X: pd.DataFrame) -> str:
        coordinates = (X[schema.lon_col].astype(str) + "," + X[schema.lat_col].astype(str))
        coordinates = ";".join(coordinates.to_list())
        return coordinates

    def __assert_inputs(self, X):
        assert isinstance(X, pd.DataFrame)
        assert schema.lat_col in X
        assert schema.lon_col in X

    def __get_osrm_service_mapping(
            self,
            mapping: dict[str, Any],
            service: str,
    ) -> str:
        try:
            return mapping[service]
        except KeyError:
            raise RuntimeError(f"Query driver is not available for service: {service}")

    @property
    def host(self):
        return self.__host

    @property
    def timeout(self):
        return self.__timeout

    def preprocess_query(self, X: pd.DataFrame, *args, **kwargs) -> str:
        """
        Fabricates url request from input gps coordinates to table osrm service

        Args:
        X (pd.DataFrame): dataframe with `latitude` and `longitude` coordinates
        *args, **kwargs: are route service parameters

        Returns:
        str: url query
        """
        self.__assert_inputs(X)
        coordinates = self.__lat_lon_df_to_url_string(X)

        params = self.__osrm_params(*args, **kwargs).url_parameters()
        url = self.__pack_url(self.__service_profile, coordinates, params)

        return url

    def query(self, url: str) -> dict[str, Any]:
        try:
            with requests.Session() as session:
                response = session.get(url, timeout=self.timeout)
                response = response.json()
                return response
        except Exception as exc:
            exception = RuntimeError(f"Failure request from osrm driver: {exc}")
            logging.error(exception)
            raise exception
