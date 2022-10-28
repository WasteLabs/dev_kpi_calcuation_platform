#!/bin/bash

status_code=$(curl --write-out %{http_code} --silent --output /dev/null -XPOST http://localhost:9000/2015-03-31/functions/function/invocations -d @.github/bash/test_event.json)

if [[ "$status_code" -ne 200 ]] ; then
  echo "Healthcheck is failed with code $status_code"
  exit 1
else
  echo "Healthcheck is passed"
fi

# curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @event.json
