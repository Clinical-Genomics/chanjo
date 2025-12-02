# -*- coding: utf-8 -*-
import pytest
from mock import patch

from chanjo.init import bootstrap
from chanjo.testutils import FakeZipFile, fake_urlretrieve


@pytest.mark.parametrize("build", ["37", "38"])
@patch("urllib.request.urlretrieve", fake_urlretrieve)
@patch("zipfile.ZipFile", FakeZipFile)
def test_pull(tmp_path, build):
    target_dir = str(tmp_path)

    # WHEN downloading resources
    bootstrap.pull(target_dir, build=build)

    # THEN BED resource should be in place
    bed_file = tmp_path.joinpath(bootstrap.BED_NAME[build])
    assert bed_file.exists()

    # Check that only this file is in the directory
    assert len(list(tmp_path.iterdir())) == 1

    # GIVEN the resources already exist
    bootstrap.pull(target_dir, build=build)
    # THEN nothing happens (file already exists)
    assert bed_file.exists()
