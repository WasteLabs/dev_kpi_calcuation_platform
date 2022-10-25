from pydantic import BaseModel, Field


class Schema(BaseModel):
    lat_col: str = Field(default="latitude", description="Latitude of coordinate")
    lon_col: str = Field(default="longitude", description="Longitude of coordinate")
