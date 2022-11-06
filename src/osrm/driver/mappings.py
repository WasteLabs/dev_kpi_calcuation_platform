from . import models


SERVICES_PROFILES = {
    "route": "route/v1/driving",
    "trip": "trip/v1/driving",
}


PARAMETERS = {
    "route": models.RouteParameters,
    "trip": models.TripParameters,
}
