from pydantic import BaseModel, Field
import pandas as pd


class Formats(BaseModel):
    datetime_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="datetime class format",
    )


class IDs(BaseModel):
    col_filename: str = Field(
        default="filename",
        description="source filename",
    )
    col_processing_datetime: str = Field(
        default="process_datetime",
        description="Processing timestamp",
    )
    col_processing_id: str = Field(
        default="processing_id",
        description="compute ID",
    )


class StopsSchema(IDs):
    dist_from_prev_point: str = Field(
        default="dist_from_prev_point_km",
        description="Travel distance from predecessing point",
    )
    dur_from_prev_point: str = Field(
        default="dur_from_prev_point_hour",
        description="Travel duration from predecessing point",
    )
    route_sequence: str = Field(
        default="route_sequence",
        description="stop visit sequence in route",
    )

    def order_stops(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.sort_values(by=[self.route_sequence]).reset_index(drop=True)


class KpiSchema(IDs):
    travel_distance: str = Field(
        default="distance_km",
        description="Total travelled distance in km",
    )
    travel_duration: str = Field(
        default="duration_hour",
        description="Total travelled duration in hours",
    )
    travel_path: str = Field(
        default="travel_path",
        description="Linestring object of travel path",
    )
