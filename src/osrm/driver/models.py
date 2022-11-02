from typing import Literal
from pydantic import Field

from ..abstract import AbstractParameters


class RouteParameters(AbstractParameters):
    overview: Literal["full", "false", "simplified"] = Field(default='full')
    steps: Literal["true", "false"] = Field(default='true')
    alternatives: Literal["true", "false"] = Field(default='false')
    geometries: Literal["polyline", "polyline6", "geojson"] = Field(default='geojson')
    annotations: Literal["true", "false"] = Field(default='true')
    continue_straight: Literal["true", "false"] = Field(default='true')


class TripParameters(AbstractParameters):
    pass
