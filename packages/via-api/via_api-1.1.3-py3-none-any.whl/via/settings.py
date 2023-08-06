import os
import pkg_resources
from packaging import version

# TODO: data from DOWNLOAD_JOURNEYS_URL should give back the s3 region
DOWNLOAD_JOURNEYS_URL = os.getenv(
    "DOWNLOAD_JOURNEYS",
    "https://l7vv5djf9h.execute-api.eu-west-1.amazonaws.com/default/getUUIDs",
)
S3_REGION = os.getenv("S3_REGION", "eu-west-1")

PREPARED_GEOJSON_BUCKET = os.getenv("PREPARED_GEOJSON_BUCKET", "via-geojson")
PREPARED_CACHE_BUCKET = os.getenv("PREPARED_CACHE_BUCKET", "via-cache")

MIN_ACC_SCORE = float(os.getenv("MIN_ACC_SCORE", "0.001"))
MIN_PER_JOURNEY_USAGE = float(os.getenv("MIN_PER_JOURNEY_USAGE", "1"))
MIN_METRES_PER_SECOND = float(
    os.getenv("MIN_METRES_PER_SECOND", "1.4")
)  # 1.4 mps is average walking speed apparently
MAX_METRES_PER_SECOND = float(
    os.getenv("MAX_METRES_PER_SECOND", "10000")
)  # Arbitrarily high, will figure out a reasonable number at some point

MIN_JOURNEY_VERSION = version.parse(os.getenv("MIN_JOURNEY_VERSION", "0.0.0"))
MAX_JOURNEY_VERSION = version.parse(os.getenv("MAX_JOURNEY_VERSION", "999.999.999"))

# How often to skip gps points, smooths things out a bit more
# 1 includes all, 3 includes every 3rd etc
# Intervals are generally 2 seconds
GPS_INCLUDE_RATIO = int(os.getenv("GPS_INCLUDE_RATIO", "2"))

NEAREST_EDGE_METHOD = os.getenv("NEAREST_EDGE_METHOD", "angle_nearest")
CLOSE_ANGLE_TO_ROAD = float(os.getenv("CLOSE_ANGLE_TO_ROAD", 20))

DEFAULT_OVERPASS_API = os.getenv("DEFAULT_OVERPASS_API", "https://overpass-api.de/api")
CUSTOM_OVERPASS_API = os.getenv("CUSTOM_OVERPASS_API", "http://54.73.95.15/api")

ENABLE_COLLISIONS = (
    True if os.getenv("ENABLE_COLLISIONS", "False").lower()[0] == "t" else False
)

CLEAN_MEMORY = os.getenv("TEST_ENV", "False") == "False"

MAX_JOURNEY_METRES_SQUARED = 5e7  # 50km^2

MAX_GEOJSON_AGE = (
    60 * 60
)  # How long to cache served geojson files before generating again (using new data)

VERSION = pkg_resources.require("via-api")[0].version
