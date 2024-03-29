from datetime import datetime
import pandas as pd
import pandera as pa

from . import nodes
from . import configs as lambda_configs
from ..configs import logger
from ...models import Formats
from ...models import KpiSchema
from ...models import StopsSchema
from ...osrm import Client
from ... import environment as env


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
        self.timestamp_id = str(datetime.now().strftime(formats.datetime_format))
        self.osrm_client = Client(host=env.OSRM_HOST)
        self.processing_id = f"{self.timestamp_id}__{self.filename}"

    def __validate_schema(self, stops: pd.DataFrame) -> pd.DataFrame:
        try:
            pandera_schema = stops_schema.factory_raw_user_stops_schema()
            return pandera_schema.validate(self.stops)
        except pa.errors.SchemaError as exc:
            msg = (f"Provided user file with incorrect schema: {exc}")
            raise RuntimeError(msg)

    def __validate_depot_points(self, stops: pd.DataFrame):
        coordinates = stops[[
            stops_schema.latitude,
            stops_schema.longitude,
        ]].to_dict("records")
        if coordinates[0] != coordinates[-1]:
            msg = (
                "Depot coordinates mismatch. Please ensure "
                "exact match of first and last points coordinates"
            )
            raise RuntimeError(msg)

    def validate_user_stops(self) -> pd.DataFrame:
        self.stops = self.__validate_schema(self.stops)
        self.__validate_depot_points(self.stops)

    def read_stops(self):
        logger.info(f"Start reading stops from: {self.source_path}")
        self.stops = nodes.read_excel_file(path=self.source_path)
        logger.info(f"Finish reading stops from: {self.source_path}")

    def __generate_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        return df \
            .pipe(lambda x: nodes.expand_name(stops=x, fname=self.filename)) \
            .pipe(lambda x: nodes.expand_processing_time(stops=x, timestamp_id=self.timestamp_id)) \
            .pipe(lambda x: nodes.expand_processing_id(stops=x, processing_id=self.processing_id))

    def process_stops(self):
        logger.info("Start processing stops")
        self.stops = self.__generate_ids(self.stops)
        self.stops[stops_schema.dur_from_prev_point] = self.osrm_route.duration_per_stop_hours
        self.stops[stops_schema.dist_from_prev_point] = self.osrm_route.distance_per_stop_km
        logger.info("Finish processing stops")

    def __solve_travelling_salesman_problem(self, col_route_seq: str):
        osrm_trip = self.osrm_client.trip(X=self.stops)
        self.stops[col_route_seq] = osrm_trip.route_sequence
        logger.info("Succesfull extraction route sequence")

    def ensure_route_sequence_presence(self):
        logger.info("Start route sequence presence ensure")
        col_route_sequence = stops_schema.route_sequence
        is_route_sequnce_provided = col_route_sequence in self.stops
        logger.info(f"Is route_sequence provided: {is_route_sequnce_provided}")
        if not is_route_sequnce_provided:
            self.__solve_travelling_salesman_problem(col_route_sequence)
        logger.info("Finish route sequence presence ensure")

    def extract_osrm_route_details(self):
        self.stops = stops_schema.order_stops(self.stops)
        self.osrm_route = self.osrm_client.route(self.stops.copy())

    def compute_kpi(self):
        logger.info("Start computing kpi")
        kpi = pd.DataFrame(
            {
                kpi_schema.travel_distance: self.osrm_route.total_distance_km,
                kpi_schema.travel_duration: self.osrm_route.total_duration_hour,
                kpi_schema.travel_path: str(self.osrm_route.linestring_coordinates),
            }, index=[0],
        )
        self.kpi = self.__generate_ids(kpi)
        logger.info("Finish computing kpi")

    def export_kpi(self):
        logger.info("Start export kpi")
        nodes.export_parquet_to_athena(
            df=self.kpi,
            **lambda_configs.KPI_WR_EXPORT_PARQUET_CONFIGS,
        )
        logger.info("Finish export kpi")

    def export_stops(self):
        logger.info("Start export stops")
        nodes.export_parquet_to_athena(
            df=self.stops,
            **lambda_configs.STOPS_WR_EXPORT_PARQUET_CONFIGS,
        )
        logger.info("Finish export stops")

    def run_lifecycle(self):
        self.read_stops()
        self.validate_user_stops()
        self.ensure_route_sequence_presence()
        self.extract_osrm_route_details()
        self.process_stops()
        self.compute_kpi()
        self.export_kpi()
        self.export_stops()
