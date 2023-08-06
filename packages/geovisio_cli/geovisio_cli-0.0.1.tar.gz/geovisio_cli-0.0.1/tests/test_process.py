import pytest
import os
from geovisio_cli import sequence
from .conftest import FIXTURE_DIR
from pathlib import Path


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "not_a_pic.md"),
)
def test_upload_with_invalid_file(datafiles):
    s = sequence.process(path=Path(datafiles))

    assert len(s.pictures) == 3
