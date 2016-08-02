# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from mock import patch
from chanjo.init import bootstrap

from test_utils import FakeZipFile, fake_urlretrieve


@patch('chanjo.compat.urlretrieve', fake_urlretrieve)
@patch('zipfile.ZipFile', FakeZipFile)
def test_pull(tmpdir):
    # GIVEN a target directory
    target_dir = str(tmpdir)
    # WHEN downloading resources
    bootstrap.pull(target_dir)
    # THEN BED resource should be in place
    out_bed = str(tmpdir.join(bootstrap.BED_NAME))
    assert os.path.exists(out_bed)
    assert len(tmpdir.listdir()) == 1

    # GIVEN the resources already exists
    bootstrap.pull(target_dir)
    # THEN nothing happens :)
