from typing import Union

import numpy as np
import pandas as pd
from shapely.geometry import LineString


from ..abstract import AbstractParser
from ..models import Schema


schema = Schema()


class RouteParser(AbstractParser):
    SEC_IN_HOURS = 3600
    METERS_IN_KILOMETER = 1000
    ROUNDING_DECIMALS = 6

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

    @property
    def total_duration_sec(self) -> Union[int, float]:
        _key_sequence = ["routes", 0, "duration"]
        return self._get_key_seq_value(
            content=self.content,
            key_sequence=_key_sequence,
        )

    @property
    def total_duration_hour(self) -> Union[int, float]:
        return round(
            self.total_duration_sec / self.SEC_IN_HOURS,
            self.ROUNDING_DECIMALS,
        )

    @property
    def total_distance_meters(self) -> Union[int, float]:
        _key_sequence = ["routes", 0, "distance"]
        return self._get_key_seq_value(
            content=self.content,
            key_sequence=_key_sequence,
        )

    @property
    def total_distance_km(self) -> Union[int, float]:
        return self.total_distance_meters / self.METERS_IN_KILOMETER

    @property
    def legs(self):
        _key_sequence = ["routes", 0, "legs"]
        return self._get_key_seq_value(
            content=self.content,
            key_sequence=_key_sequence,
        )

    def __mark_start_point(self, parameter: list[float]):
        """
        Adds 0 to distance or time to indicating a starting point
        """
        return [0] + parameter

    @property
    def distance_per_stop_meters(self):
        distances = list(
            map(
                lambda x: x["distance"],
                self.legs,
            ),
        )
        return self.__mark_start_point(distances)

    @property
    def distance_per_stop_km(self):
        distance = np.array(self.distance_per_stop_meters) / self.METERS_IN_KILOMETER
        return distance.tolist()

    @property
    def duration_per_stop_meters(self):
        duration = list(
            map(
                lambda x: x["duration"],
                self.legs,
            ),
        )
        return self.__mark_start_point(duration)

    @property
    def duration_per_stop_hours(self):
        duration = np.array(self.duration_per_stop_meters) / self.SEC_IN_HOURS
        duration = duration.round(self.ROUNDING_DECIMALS)
        return duration.tolist()
