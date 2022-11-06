from typing import Literal
from pydantic import Field

from ..abstract import AbstractParameters


class RouteParameters(AbstractParameters):
    overview: Literal["full", "false", "simplified"] = Field(
        default='full',
        description=(
            "Add overview geometry either full, simplified according"
            " to highest zoom level it could be display on, or not at all."
        ),
    )
    steps: Literal["true", "false"] = Field(
        default='true',
        description="Returned route instructions for each trip",
    )
    alternatives: Literal["true", "false"] = Field(
        default='false',
        description=(
            "Search for alternative routes. Passing a number"
            " alternatives=n searches for up to n alternative routes. *"
        ),
    )
    geometries: Literal["polyline", "polyline6", "geojson"] = Field(
        default='geojson',
        description="Returned route geometry format (influences overview and per step)",
    )
    annotations: Literal["true", "false"] = Field(
        default='true',
        description="Returns additional metadata for each coordinate along the route geometry.",
    )
    continue_straight: Literal["true", "false"] = Field(
        default='true',
        description=(
            "Forces the route to keep going straight at waypoints constraining "
            "uturns there even if it would be faster. Default value depends on the profile."
        ),
    )


class TripParameters(AbstractParameters):
    """
    NOTE: in default behavior we specify duplicated depot point as first and last points
    """
    roundtrip: Literal["true", "false"] = Field(
        default='false',
        description="Returned route is a roundtrip (route returns to first location)",
    )
    source: Literal["any", "first"] = Field(
        default='first',
        description="Returned route starts at any or first coordinate",
    )
    destination: Literal["any", "last"] = Field(
        default='last',
        description="Returned route ends at any or last coordinate",
    )
    steps: Literal["true", "false"] = Field(
        default='true',
        description="Returned route instructions for each trip",
    )
    geometries: Literal["polyline", "polyline6", "geojson"] = Field(
        default='geojson',
        description="Returned route geometry format (influences overview and per step)",
    )
    annotations: Literal["true", "false"] = Field(
        default='true',
        geometries="Returns additional metadata for each coordinate along the route geometry.",
    )
    overview: Literal["full", "false", "simplified"] = Field(
        default='full',
        description=(
            "Add overview geometry either full, simplified according"
            " to highest zoom level it could be display on, or not at all."
        ),
    )
