import logging
import sys

from .session import Session


root = logging.getLogger()
root.setLevel(logging.INFO)

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s :::')
log_handler.setFormatter(formatter)
root.addHandler(log_handler)


def fabricate_source_file_path(event) -> str:
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    return f"s3://{bucket}/{file_key}"


def handler(event, context):
    session = Session(source_path=fabricate_source_file_path(event))
    session.run_lifecycle()
