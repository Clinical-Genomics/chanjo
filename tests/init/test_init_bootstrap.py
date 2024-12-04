# -*- coding: utf-8 -*-
from mock import patch

from chanjo.init import bootstrap
from chanjo.testutils import FakeZipFile, fake_urlretrieve


@patch('urllib.request.urlretrieve', fake_urlretrieve)
@patch('zipfile.ZipFile', FakeZipFile)
def test_pull(tmp_path):
    # GIVEN a target directory
    target_dir = str(tmp_path)
    # WHEN downloading resources
    bootstrap.pull(target_dir)
    # THEN BED resource should be in place
    out_bed = tmp_path.joinpath(bootstrap.BED_NAME)
    assert out_bed.exists()
    assert len(list(tmp_path.iterdir())) == 1

    # GIVEN the resources already exists
    bootstrap.pull(target_dir)
    # THEN nothing happens :)
