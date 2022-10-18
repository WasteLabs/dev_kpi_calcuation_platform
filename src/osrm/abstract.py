from abc import ABC, abstractmethod
import logging
from typing import Any

from pydantic import BaseModel
import requests


class AbstractQueryDriver(ABC):

    def __init__(self, host: str, timeout: int):
        self.__host = host
        self.__timeout = timeout

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

    @property
    def host(self):
        return self.__host

    @property
    def timeout(self):
        return self.__timeout

    def _pack_url(self, service: str, coordinates: str, params: str) -> str:
        return f"{self.host}/{service}/{coordinates}{params}"

    @abstractmethod
    def preprocess_query(self, *args, **kwargs) -> str:
        """
        Function organizing query factory
        """
        pass


class AbstractParameters(BaseModel):

    def url_parameters(self):
        params = self.__dict__
        params = list(
            map(
                lambda x, y: f"{x}={y}",
                params.keys(),
                params.values(),
            ),
        )
        return "?" + "&".join(params)
