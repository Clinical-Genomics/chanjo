# -*- coding: utf-8 -*-
import logging
import subprocess

from subprocess import CalledProcessError

log = logging.getLogger(__name__)


def run_sambamba(bam_file, region_file, outfile=None, cov_thresholds=()):
    """Run sambamba from Chanjo.

    Args:
        bam_file (Path): path to the BAM alignment file
        region_file (Path): path to the input BED file defining exon regions
        outfile (Optional[Path]): file to write to (otherwise STDOUT)
        cov_thresholds (Optional[List[int]]): levels to sample completeness at
    """
    sambamba_call = ['sambamba', 'depth', 'region', '--regions', region_file, bam_file]

    if outfile:
        sambamba_call += ['-o', outfile]

    for coverage_threshold in cov_thresholds:
        sambamba_call += ['-T', str(coverage_threshold)]

    log.info("Running sambamba with call: %s", ' '.join(sambamba_call))
    try:
        subprocess.check_call(sambamba_call)  # stderr=log_stream
    except OSError as error:
        log.critical("sambamba seems to not exist on your system.")
        raise error
    except CalledProcessError as error:  # pragma: no cover
        log.critical("Something went wrong when running sambamba. "
                     "Please see sambamba error output.")
        raise error

    log.debug("sambamba ran successfully")
