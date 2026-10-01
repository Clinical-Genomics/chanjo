# -*- coding: utf-8 -*-
import logging

import click

from chanjo.sex import sex_from_bam

LOG = logging.getLogger(__name__)


@click.command()
@click.option("-p", "--prefix", default="", help="chromosome prefix")
@click.option(
    "-b",
    "--build",
    type=click.Choice(["37", "38"]),
    default="37",
    show_default=True,
    help="Genome version to use.",
)
@click.argument("bam_path", type=click.Path(exists=True))
@click.pass_context
def sex(context, prefix, bam_path, build):
    """Guess the sex of a BAM alignment."""
    try:
        result = sex_from_bam(bam_path, prefix=prefix, build=build)
    except Exception:
        LOG.exception("Something went really wrong :(")
        context.abort()

    # print the results to the console for pipeability (csv)
    click.echo("#{prefix}X_coverage\t{prefix}Y_coverage\tsex".format(prefix=prefix))
    click.echo("\t".join(map(str, result)))
