from pydantic import BaseModel, Field


class StopsSchema(BaseModel):
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
    datetime_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="datetime class format",
    )
