import pandas as pd

from src.osrm.driver import QueryDriver
from src.osrm.parsers.route import RouteParser


class Client(object):

    def __init__(self, host: str, timeout: int = 5):
        self.__driver_route = QueryDriver(host=host, timeout=timeout, service="route")

    def route(self, X: pd.DataFrame,  *args, **kwargs):
        """
        Function

        Args:
        X (pd.DataFrame): coordinates dataframe
            with `latitude` and `longitude` columns
        *args, **kwargs available options:
            overview: Literal["full", "false", "simplified"] = Field(default='full')
            steps: Literal["true", "false"] = Field(default='true')
            alternatives: Literal["true", "false"] = Field(default='false')
            geometries: Literal["polyline", "polyline6", "geojson"] = Field(default='geojson')
            annotations: Literal["true", "false"] = Field(default='true')
            continue_straight: Literal["true", "false"] = Field(default='true')
        """
        url_query = self.__driver_route.preprocess_query(X, *args, **kwargs)
        response = self.__driver_route.query(url=url_query)
        return RouteParser(content=response)

    def match(self):
        raise NotImplementedError("Functionality is not implemented yet.")

    def table(self):
        raise NotImplementedError("Functionality is not implemented yet.")
