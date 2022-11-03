from .session import Session
from ...middleware import execute_session_with_status_log


def fabricate_source_file_path(event) -> str:
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    return f"s3://{bucket}/{file_key}"


def handler(event, context):
    session = Session(source_path=fabricate_source_file_path(event))
    execute_session_with_status_log(
        session,
        event=event,
        context=context,
    )
