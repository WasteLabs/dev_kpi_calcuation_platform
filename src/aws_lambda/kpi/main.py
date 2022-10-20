import logging
import os
import json


def handler(event, context):

    json_region = os.environ['AWS_REGION']
    body_content = {
        "Region ": json_region,
        "event": event,
        "type :: event": str(type(event)),
        "type :: context": str(type(context)),
    }
    logging.info(body_content)
    print(body_content)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body_content),
    }
