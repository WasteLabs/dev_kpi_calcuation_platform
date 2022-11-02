from typing import Union
import pandas as pd

from src.osrm.driver import QueryDriver
from src.osrm.parsers.route import RouteParser
from src.osrm.parsers.trip import TripParser


class Client(object):

    OSRM_ROUTE_SERVICE = "route"
    OSRM_TRIP_SERVICE = "trip"

    def __init__(self, host: str, timeout: int = 10):
        self.__host = host
        self.__timeout = timeout

    def __perform_extraction(
        self,
        service: str,
        X: pd.DataFrame,
        parser: Union[RouteParser, TripParser],
        *args, **kwargs,
    ) -> Union[RouteParser, TripParser]:
        driver = QueryDriver(
            host=self.__host,
            timeout=self.__timeout,
            service=service,
        )
        url_query = driver.preprocess_query(X, *args, **kwargs)
        response = driver.query(url=url_query)
        return parser(content=response)

    def route(self, X: pd.DataFrame,  *args, **kwargs):
        """
        Function organizing interaction with `route` service

        Args:
        X (pd.DataFrame): coordinates dataframe with `latitude`, `longitude` fields
        *args, **kwargs are available under osrm.driver.models.RouteParameters
        """
        return self.__perform_extraction(
            service=self.OSRM_ROUTE_SERVICE,
            X=X,
            parser=RouteParser,
            *args, **kwargs,
        )

    def trip(self, X: pd.DataFrame,  *args, **kwargs):
        """
        Function organizing interaction with `trip` service

        Args:
        X (pd.DataFrame): coordinates dataframe with `latitude` and `longitude` columns
        *args, **kwargs are available under osrm.driver.models.RouteParameters
        """
        return self.__perform_extraction(
            service=self.OSRM_TRIP_SERVICE,
            X=X.copy(),
            parser=TripParser,
            *args, **kwargs,
        )

    def match(self):
        raise NotImplementedError("Functionality is not implemented yet.")

    def table(self):
        raise NotImplementedError("Functionality is not implemented yet.")
