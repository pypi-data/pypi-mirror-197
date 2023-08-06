import os
import shutil
import glob
import multiprocessing

import boto3
import requests
from botocore import UNSIGNED
from botocore.client import Config

from via import logger
from via.settings import DOWNLOAD_JOURNEYS_URL, S3_REGION
from via.constants import REMOTE_DATA_DIR
from via.models.journey import Journey


S3_CLIENT = None


def download_journey(data):
    if S3_CLIENT is None:
        s3 = boto3.client(
            "s3", region_name=S3_REGION, config=Config(signature_version=UNSIGNED)
        )

    filename = data["filename"]
    log_geo = data["log_geo"]
    cache_graphs = data["cache_graphs"]

    journey_id = os.path.splitext(filename)[0]

    tmp_filepath = f"/tmp/{journey_id}.json"

    s3.download_file("bike-road-quality", filename, tmp_filepath)

    journey = Journey.from_file(tmp_filepath)

    if not journey.has_enough_data:
        logger.warning(f"Journey {journey_id} has not enough data")
        return

    if log_geo:
        geo = journey.origin.gps.reverse_geo
        logger.info(
            f'Pulled journey from: {geo["cc"]}, {geo["place_3"]}, {geo["place_2"]}, {geo["place_1"]}'
        )

    if cache_graphs:
        logger.info(f"Caching graphs for {journey_id}")
        journey.bounding_graph

    local_filepath = os.path.join(
        REMOTE_DATA_DIR, journey.transport_type.lower(), filename
    )
    logger.info(f"Putting to {local_filepath}")

    os.makedirs(os.path.dirname(local_filepath), exist_ok=True)

    shutil.move(tmp_filepath, local_filepath)


def get_journey_files():
    return requests.get(DOWNLOAD_JOURNEYS_URL).json()


def get_journey_files_to_download():
    journey_ids = []
    for filename in glob.iglob(REMOTE_DATA_DIR + "/**/*", recursive=True):
        journey_ids.append(os.path.splitext(os.path.basename(filename))[0])

    journey_files_to_download = []
    for filename in get_journey_files():
        journey_id = os.path.splitext(os.path.basename(filename))[0]
        if journey_id in journey_ids:
            continue
        journey_files_to_download.append(filename)

    return journey_files_to_download


def pull_journeys(cache_graphs=False, log_geo=False):
    """

    :kwargs cache_graphs: cache the graphs of pulled journeys so we don't
        need to do it again later when we need them
    :log_geo: to log geographical data or not. Logging this slows down
        the pulling
    """

    if not os.path.exists(REMOTE_DATA_DIR):
        os.makedirs(REMOTE_DATA_DIR, exist_ok=True)

    journey_files_to_download = get_journey_files_to_download()

    logger.info(f"Downloading {len(journey_files_to_download)} files")

    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        pool.map(
            download_journey,
            [
                {"filename": filename, "cache_graphs": cache_graphs, "log_geo": log_geo}
                for filename in journey_files_to_download
            ],
        )
