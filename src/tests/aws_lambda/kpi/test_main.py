from typing import Any
import pytest


from src.aws_lambda.kpi.main import handler


@pytest.fixture
def correct_event() -> dict[str, Any]:
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
                        "name": "kpi-calculation-platform",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE",
                        },
                        "arn": "arn:aws:s3:::example-bucket",
                    },
                    "object": {
                        "key": "test/01_raw/user_stops/stops_without_sequence.xlsx",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901",
                    },
                },
            },
        ],
    }


@pytest.fixture
def incorrect_schema_file_event() -> dict[str, Any]:
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
                        "name": "kpi-calculation-platform",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE",
                        },
                        "arn": "arn:aws:s3:::example-bucket",
                    },
                    "object": {
                        "key": "test/01_raw/user_stops/incorrect_schema_stops.xlsx",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901",
                    },
                },
            },
        ],
    }


class TestMain:

    def test_hander_on_correct_file(self, correct_event: dict[str, Any]):
        status = handler(event=correct_event, context={})
        assert status.to_dict("records")[0]["status"] == "successfull"

    def test_hander_on_incorrect_schema_file(self, incorrect_schema_file_event: dict[str, Any], s3_fname: str):
        status = handler(event=incorrect_schema_file_event, context={})
        assert status.to_dict("records")[0]["status"] == "failure"
