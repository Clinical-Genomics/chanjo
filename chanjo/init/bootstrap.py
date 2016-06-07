# -*- coding: utf-8 -*-
import logging
import urllib
import zipfile

from path import path

DB_NAME = 'coverage.ccds15.grch37p13.extended.sqlite3'
DATABASE_URL = ("https://s3.eu-central-1.amazonaws.com/chanjo/{}"
                .format(DB_NAME))
BED_NAME = 'ccds15.grch37p13.extended.bed'
BED_URL = ("https://s3.eu-central-1.amazonaws.com/"
           "chanjo/ccds15.grch37p13.extended.bed.zip")

logger = logging.getLogger(__name__)


def pull(target_dir, force=False):  # pragma: no cover
    """Download precompiled resources into a folder.

    Args:
        target_dir (path): relative path the folder to download to
        force (Optional[bool]): whether to overwrite existing files
    """
    logger.debug('ensure target directory exists')
    target_path = path(target_dir)
    target_path.makedirs_p()

    db_path = target_path.joinpath(DB_NAME)
    bed_zip_path = target_path.joinpath("{}.zip".format(BED_NAME))
    final_bed = target_path.joinpath(BED_NAME)

    if not path(db_path).exists() or force:
        logger.info('downloading... [%s]', BED_URL)
        urllib.urlretrieve(DATABASE_URL, db_path)
    else:
        logger.warn('file already exists, skipping: %s', db_path)

    if not final_bed.exists() or force:
        logger.info('downloading... [%s]', BED_URL)
        urllib.urlretrieve(BED_URL, bed_zip_path)

        logger.info('extracting BED file...')
        zip_ref = zipfile.ZipFile(bed_zip_path, 'r')
        zip_ref.extractall(target_dir)

        logger.info('removing BED archive...')
        bed_zip_path.remove_p()
    else:
        logger.warn('file already exists, skipping: %s', final_bed)
