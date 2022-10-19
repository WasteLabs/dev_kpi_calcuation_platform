import pytest


@pytest.fixture
def s3_sample_path() -> str:
    return (
        "s3://dev-data-temp/dev_kpi_calculation_platform/dev"
        "/01_raw/test_stops.xlsx"
    )


@pytest.fixture
def s3_fname() -> str:
    return "test_stops.xlsx"
