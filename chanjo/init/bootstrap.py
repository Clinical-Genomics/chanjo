# -*- coding: utf-8 -*-
import logging
import sys
import zipfile
from pathlib import Path

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


DB_NAME = "chanjo.coverage.sqlite3"
BED_NAME = {"37": "hgnc.grch37p13.exons.bed", "38": "hgnc.grch38p14.exons.bed"}
BED_URL = {
    "37": "https://s3.eu-central-1.amazonaws.com/clinical-assets/hgnc.grch37p13.exons.bed.zip",
    "38": "https://figshare.com/ndownloader/files/60037697",
}

logger = logging.getLogger(__name__)


def pull(target_dir, force=False, build="37"):  # pragma: no cover
    """Download precompiled resources into a folder.

    Args:
        target_dir (path): relative path the folder to download to
        force (Optional[bool]): whether to overwrite existing files
    """
    logger.debug("ensure target directory exists")
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    bed_zip_path = target_path.joinpath("{}.zip".format(BED_NAME[build]))
    final_bed = target_path.joinpath(BED_NAME[build])

    if not final_bed.exists() or force:
        logger.info("downloading... [%s]", BED_URL[build])
        urlretrieve(BED_URL[build], bed_zip_path)

        logger.info("extracting BED file...")
        zip_ref = zipfile.ZipFile(bed_zip_path, "r")
        zip_ref.extractall(target_dir)

        logger.info("removing BED archive...")
        bed_zip_path.unlink()
    else:
        logger.warn("file already exists, skipping: %s", final_bed)
