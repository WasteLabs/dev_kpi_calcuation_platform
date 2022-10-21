import logging
from datetime import datetime
import pandas as pd

from . import nodes
from ...models import Formats
from ...models import KpiSchema
from ...models import StopsSchema
from ...osrm import Client
from ... import environment as env
from . import configs as lambda_configs


logger = logging.getLogger(__name__)
formats = Formats()
stops_schema = StopsSchema()
kpi_schema = KpiSchema()


class Session(object):
    """
    Class organizing lambda function lifecycle
    """

    def __init__(self, source_path: str):
        assert type(source_path) is str
        self.source_path = source_path
        self.filename = source_path.rsplit("/", 1)[1]
        self.timestamp_id = datetime.now().strftime(formats.datetime_format)
        self.client = Client(host=env.OSRM_HOST)

    def read_stops(self):
        logger.info(f"Start reading stops from: {self.source_path}")
        self.stops = nodes.read_excel_file(path=self.source_path)
        logger.info(f"Finish reading stops from: {self.source_path}\n")

    def __generate_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        return df \
            .pipe(lambda x: nodes.expand_name(stops=x, fname=self.filename)) \
            .pipe(lambda x: nodes.expand_processing_time(stops=x, timestamp_id=self.timestamp_id)) \
            .pipe(nodes.generate_id)

    def process_stops(self):
        logger.info("Start processing stops")
        self.stops = self.__generate_ids(self.stops)
        logger.info("Finish processing stops\n")

    def compute_kpi(self):
        logger.info("Start computing kpi")
        route = self.client.route(self.stops.copy())
        kpi = pd.DataFrame(
            {
                kpi_schema.travel_distance: route.total_distance_km,
                kpi_schema.travel_duration: route.total_duration_hour,
                kpi_schema.travel_path: str(route.linestring_coordinates),
            }, index=[0],
        )
        self.kpi = self.__generate_ids(kpi)
        logger.info("Finish computing kpi\n")

    def export_kpi(self):
        logger.info("Start export kpi")
        nodes.export_parquet_to_athena(
            df=self.kpi,
            **lambda_configs.KPI_WR_EXPORT_PARQUET_CONFIGS,
        )
        logger.info("Finish export kpi\n")

    def export_stops(self):
        logger.info("Start export stops")
        nodes.export_parquet_to_athena(
            df=self.stops,
            **lambda_configs.STOPS_WR_EXPORT_PARQUET_CONFIGS,
        )
        logger.info("Finish export stops\n")
