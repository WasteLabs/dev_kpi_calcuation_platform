from typing import Any
import pytest


from src.aws_lambda.kpi.main import handler


@pytest.fixture
def test_event() -> dict[str, Any]:
    return {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "ap-southeast-1",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "EXAMPLE",
                },
                "requestParameters": {
                    "sourceIPAddress": "127.0.0.1",
                },
                "responseElements": {
                    "x-amz-request-id": "EXAMPLE123456789",
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "dev-data-temp",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE",
                        },
                        "arn": "arn:aws:s3:::example-bucket",
                    },
                    "object": {
                        "key": "dev_kpi_calculation_platform/dev/01_raw/test_stops.xlsx",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901",
                    },
                },
            },
        ],
    }


class TestMain:

    def test_hander(self, test_event: dict[str, Any], s3_fname: str):
        handler(event=test_event, context={})
