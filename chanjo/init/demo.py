# -*- coding: utf-8 -*-
import logging
import shutil
from errno import EEXIST
from pathlib import Path

try:
    from importlib.resources import files
except ImportError:  # Backport support for importlib metadata on Python 3.7
    from importlib_resources import files


DEMO_BED_NAME = "hgnc.min.bed"
log = logging.getLogger(__name__)


def setup_demo(location, force=False):
    """Copy demo files to a directory.

    LOCATION: directory to add demo files to (default: ./chanjo-demo)
    """
    target_dir = Path(location)
    pkg_dir = __name__.rpartition(".")[0]

    # Get the demo-files directory path using importlib.resources
    demo_dir = files(pkg_dir) / "demo-files"

    if not demo_dir.is_dir():
        log.error("Demo files directory does not exist")
        raise FileNotFoundError(f"'demo-files' directory not found in package {pkg_dir}")

    # Check for existing files and avoid overwriting unless `force` is True
    for demo_file in demo_dir.iterdir():
        target_file_path = target_dir / demo_file.name
        if not force and target_file_path.exists():
            log.error("%s exists, pick a different location", target_file_path)
            raise OSError(EEXIST, "file already exists", target_file_path)

    try:
        # Copy the directory tree
        shutil.copytree(demo_dir, target_dir)
    except FileExistsError:
        log.warning("Location must be a non-existing directory")
        raise
    except OSError as error:
        log.error("An error occurred during file copying: %s", error)
        raise

    # Inform the user
    log.info("Successfully copied demo files to %s", target_dir)
