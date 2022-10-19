import pandas as pd
import pytest


from src.aws_lambda.kpi.session import Session


@pytest.fixture
def session(s3_sample_path: str):
    return Session(source_path=s3_sample_path)


class TestSession:

    def test_init(self, s3_sample_path: str, s3_fname: str):
        session = Session(source_path=s3_sample_path)
        assert s3_fname == session.filename

    def test_read_stops(self, session: Session):
        session.read_stops()
        assert "stops" in session.__dict__
        assert isinstance(session.stops, pd.DataFrame)
