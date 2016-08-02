import subprocess
import logging

from subprocess import CalledProcessError

log = logging.getLogger(__name__)


def run_sambamba(bam_file, region_file, outfile=None, cov_treshold=()):
    """Run sambamba from chanjo."""
    sambamba_call = [
        "sambamba",
        "depth",
        "region",
        "--regions",
        region_file,
        bam_file
    ]

    if outfile:
        sambamba_call += ['-o', outfile]

    for coverage_treshold in cov_treshold:
        sambamba_call += ['-T', str(coverage_treshold)]

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
