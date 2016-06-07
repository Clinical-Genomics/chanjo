# -*- coding: utf-8 -*-
import os

import pytest

from chanjo.init import demo


def test_setup_demo(tmpdir):
    # GIVEN a non-existing target directory
    target_dir = tmpdir.join('chanjo-demo')
    target_path = str(target_dir)
    demo.setup_demo(target_path)
    files = os.listdir(target_path)
    expected_files = os.listdir('chanjo/init/demo-files')
    assert files == expected_files

    # GIVEN the files are already in place
    with pytest.raises(OSError):
        demo.setup_demo(target_path)


def test_setup_demo_existing_dir(tmpdir):
    with pytest.raises(OSError):
        demo.setup_demo(str(tmpdir))
