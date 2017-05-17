# -*- coding: utf-8 -*-
from errno import EEXIST
import logging
from pkg_resources import resource_filename, resource_listdir

from path import Path

DEMO_BED_NAME = 'hgnc.min.bed'
log = logging.getLogger(__name__)


def setup_demo(location, force=False):
    """Copy demo files to a directory.

    \b
    LOCATION: directory to add demofiles to (default: ./chanjo-demo)
    """
    target_dir = Path(location)
    pkg_dir = __name__.rpartition('.')[0]
    demo_dir = Path(resource_filename(pkg_dir, 'demo-files'))

    # make sure we don't overwrite exiting files
    for demo_file in resource_listdir(pkg_dir, 'demo-files'):
        target_file_path = target_dir.joinpath(demo_file)
        if not force and target_file_path.exists():
            log.error("%s exists, pick a different location", target_file_path)
            raise OSError(EEXIST, 'file already exists', target_file_path)

    try:
        # we can copy the directory(tree)
        demo_dir.copytree(target_dir)
    except OSError as error:
        log.warn('location must be a non-existing directory')
        raise error

    # inform the user
    log.info("successfully copied demo files to %s", target_dir)
