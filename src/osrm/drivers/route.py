import pandas as pd

from ..abstract import AbstractQueryDriver
from ..models import Schema
from .models import RouteParameters


schema = Schema()


class RouteQueryDriver(AbstractQueryDriver):

    SERVICE = "route/v1/driving"

    def __init__(self, host: str, timeout: int = 5):
        super().__init__(host=host, timeout=timeout)

    def __lat_lon_df_to_url_string(self, X: pd.DataFrame) -> str:
        coordinates = (X[schema.lon_col].astype(str) + "," + X[schema.lat_col].astype(str))
        coordinates = ";".join(coordinates.to_list())
        return coordinates

    def __assert_inputs(self, X):
        assert isinstance(X, pd.DataFrame)
        assert schema.lat_col in X
        assert schema.lon_col in X

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

        params = RouteParameters(*args, **kwargs).url_parameters()
        url = self._pack_url(self.SERVICE, coordinates, params)

        return url
