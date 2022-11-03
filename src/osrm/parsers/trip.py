import pandas as pd

from ..abstract import AbstractParser
from ..models import Schema


schema = Schema()


class TripParser(AbstractParser):

    @property
    def waypoints(self) -> pd.DataFrame:
        _key_sequence = ["waypoints"]
        waypoints = self._get_key_seq_value(
            content=self.content,
            key_sequence=_key_sequence,
        )
        return pd.DataFrame(waypoints)

    @property
    def route_sequence(self) -> list[int]:
        return self._get_pandas_field(df=self.waypoints, key="waypoint_index")
