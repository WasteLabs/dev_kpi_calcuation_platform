from typing import Literal
from pydantic import Field

from ..abstract import AbstractParameters


class RouteParameters(AbstractParameters):
    geometry: Literal["polyline", "polyline6", "geojson"] = Field(default='geojson')
    overview: Literal["full", "false", "simplified"] = Field(default='full')
    steps: Literal["true", "false"] = Field(default='true')
    alternatives: Literal["true", "false"] = Field(default='true')
    annotations: Literal["true", "false"] = Field(default='true')
    continue_straight: Literal["true", "false"] = Field(default='true')
