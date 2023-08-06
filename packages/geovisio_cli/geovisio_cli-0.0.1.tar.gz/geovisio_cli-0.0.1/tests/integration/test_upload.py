import os
import pytest
from ..conftest import FIXTURE_DIR
from pathlib import Path
import requests
from geovisio_cli import sequence
import time


def poll_readyness(collection: str):
    """
    Wait for a collection to not be preparing.
    items wil either be 'ready' or 'broken'
    """
    waiting_time = 0.5
    nb_attempt = 300
    status = {}
    for _ in range(0, nb_attempt):
        status = sequence.get_collection_status(collection)
        if all(i["status"] != "preparing" for i in status["items"]):
            return status
        time.sleep(waiting_time)
    raise Exception(
        f"collection {str} is not ready after {nb_attempt*waiting_time}s: status {status}"
    )


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_valid_upload(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    assert len(collection.uploaded_pictures) == 3
    assert len(collection.errors) == 0

    status = poll_readyness(collection.location)
    # 3 pictures should have been uploaded
    items = status["items"]
    assert len(items) == 3

    for i in items:
        assert i["status"] == "ready"

    # the collection should also have 3 items
    collection = requests.get(f"{collection.location}/items")
    collection.raise_for_status()

    features = collection.json()["features"]
    assert len(features) == 3


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_invalid_file(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    # Only 3 pictures should have been uploaded, 1 is in error
    assert len(collection.uploaded_pictures) == 3
    assert len(collection.errors) == 1

    # But the collection status should have 3 items (and be valid)
    status = poll_readyness(collection.location)
    items = status["items"]
    assert len(items) == 3
    assert all([i["status"] == "ready" for i in items])

    # the collection should also have 3 items
    collection = requests.get(f"{collection.location}/items")
    collection.raise_for_status()
    features = collection.json()["features"]
    assert len(features) == 3


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_no_valid_file(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    assert len(collection.uploaded_pictures) == 0
    assert len(collection.errors) == 1

    status = requests.get(f"{collection.location}/geovisio_status")
    assert (
        status.status_code == 404
    )  # TODO: For the moment geovisio return a 404, we it should return a valid status response with the sequence status

    items = requests.get(f"{collection.location}/items")
    items.raise_for_status()
    features = items.json()["features"]
    assert len(features) == 0
