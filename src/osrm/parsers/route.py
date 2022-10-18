from ..abstract import AbstractParser
from ..models import Schema

from shapely.geometry import LineString
import pandas as pd


schema = Schema()


class RouteParser(AbstractParser):

    @property
    def coordinates(self) -> list[list[float]]:
        _key_sequence = ["routes", 0, "geometry", "coordinates"]
        return self._get_key_seq_value(
            content=self.content,
            key_sequence=_key_sequence,
        )

    @property
    def df_coordinates(self) -> list[list[float]]:
        return pd.DataFrame(
            self.coordinates,
            columns=[schema.lon_col, schema.lat_col],
        )

    @property
    def linestring_coordinates(self) -> LineString:
        return LineString(coordinates=self.coordinates)
