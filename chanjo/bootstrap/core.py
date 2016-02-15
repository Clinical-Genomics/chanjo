# -*- coding: utf-8 -*-
import logging
import urllib
import zipfile

from path import path

from .constants import BED_URL, DATABASE_URL, DB_NAME

logger = logging.getLogger(__name__)


def pull(target_dir, force=False):
    """Download precompiled resources into a folder."""
    logger.debug('ensure target directory exists')
    target_path = path(target_dir)
    target_path.makedirs_p()

    db_path = target_path.joinpath(DB_NAME)
    bed_path = target_path.joinpath('ccds.bed.zip')
    final_bed = target_path.joinpath('ccds.15.grch37p13.extended.bed')

    if not path(db_path).exists() or force:
        logger.info('downloading... [%s]', BED_URL)
        urllib.urlretrieve(DATABASE_URL, db_path)
    else:
        logger.warn('file already exists, skipping: %s', db_path)

    if not final_bed.exists() or force:
        logger.info('downloading... [%s]', BED_URL)
        urllib.urlretrieve(BED_URL, bed_path)

        logger.info('extracting BED file...')
        zip_ref = zipfile.ZipFile(bed_path, 'r')
        zip_ref.extractall(target_dir)

        logger.info('removing BED archive...')
        bed_path.remove_p()
    else:
        logger.warn('file already exists, skipping: %s', final_bed)
