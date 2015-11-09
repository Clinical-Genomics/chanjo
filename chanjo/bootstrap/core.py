# -*- coding: utf-8 -*-
import logging
import urllib
import zipfile

from path import path

from .constants import BED_URL, DATABASE_URL

logger = logging.getLogger(__name__)


def pull(target_dir, force=False):
    """Download precompiled resources into a folder."""
    logger.debug('ensure target directory exists')
    target_path = path(target_dir)
    target_path.makedirs_p()

    database_path = target_path.joinpath('coverage.sqlite3')
    bed_path = target_path.joinpath('ccds.bed.zip')

    files = ((database_path, DATABASE_URL), (bed_path, BED_URL))
    for file_path, url in files:
        if path(file_path).exists() and not force:
            logger.warn('file already exists, skipping: %s', file_path)
        else:
            logger.info('downloading... [%s]', url)
            urllib.urlretrieve(url, file_path)

    logger.info('extracting BED file...')
    zip_ref = zipfile.ZipFile(bed_path, 'r')
    zip_ref.extractall(target_dir)

    logger.info('removing BED archive...')
    bed_path.remove_p()
