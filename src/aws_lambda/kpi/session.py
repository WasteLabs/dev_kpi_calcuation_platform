from datetime import datetime
import pandas as pd

from . import nodes
from ...models import StopsSchema


schema = StopsSchema()


class Session(object):
    """
    Class organizing lambda function lifecycle
    """

    def __init__(self, source_path: str):
        assert type(source_path) is str
        self.source_path = source_path
        self.filename = source_path.rsplit("/", 1)[1]
        self.timestamp_id = datetime.now().strftime(schema.datetime_format)

    def read_stops(self):
        self.stops = nodes.read_excel_file(path=self.source_path)

    def __generate_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        return df \
            .pipe(lambda x: nodes.expand_name(stops=x, fname=self.filename)) \
            .pipe(lambda x: nodes.expand_processing_time(stops=x, timestamp_id=self.timestamp_id)) \
            .pipe(nodes.generate_id)

    def process_stops(self):
        self.stops = self.__generate_ids(self.stops)
