# -*- coding: utf-8 -*-
import codecs
import logging
from pathlib import Path
from shutil import which

import click
import yaml

from chanjo.init.bootstrap import BED_NAME, DB_NAME, pull
from chanjo.init.demo import DEMO_BED_NAME, setup_demo
from chanjo.store.api import ChanjoDB

LOG = logging.getLogger(__name__)


@click.command()
@click.option("-f", "--force", is_flag=True, help="overwrite existing files")
@click.option("-d", "--demo", is_flag=True, help="copy demo files")
@click.option("-a", "--auto", is_flag=True)
@click.option(
    "-b",
    "--build",
    type=click.Choice(["37", "38"]),
    default="37",
    show_default=True,
    help="Genome version to use.",
)
@click.argument("root_dir", default=".", required=False)
@click.pass_context
def init(context, force, demo, auto, build, root_dir):
    """Bootstrap a new chanjo setup."""
    is_bootstrapped = False
    root_path = Path(root_dir)

    LOG.info("setting up chanjo under: %s", root_path)
    db_uri = context.obj.get("database")
    db_uri = db_uri or "sqlite:///{}".format(root_path.joinpath(DB_NAME).resolve())

    # test setup of sambamba
    sambamba_bin = which("sambamba")
    if sambamba_bin is None:  # pragma: no cover
        LOG.warning("'sambamba' command not found")
    else:
        LOG.debug("'sambamba' found: %s", sambamba_bin)

    if demo:
        LOG.info("copying demo files: %s", root_dir)
        setup_demo(root_dir, force=force)

        LOG.info("configure new chanjo database: %s", db_uri)
        chanjo_db = ChanjoDB(db_uri)
        chanjo_db.set_up()
        is_bootstrapped = True
    elif auto or click.confirm("Bootstrap HGNC transcript BED?"):
        pull(root_dir, force=force, build=build)

        LOG.info("configure new chanjo database: %s", db_uri)
        chanjo_db = ChanjoDB(db_uri)
        chanjo_db.set_up()
        is_bootstrapped = True

    # setup config file
    root_path.mkdir(parents=True, exist_ok=True)
    conf_path = root_path.joinpath("chanjo.yaml")
    with open(conf_path, "w") as conf_handle:
        data = {"database": db_uri}
        LOG.info("writing config file: %s", conf_path)
        yaml.dump(data, conf_handle, default_flow_style=False)

    if is_bootstrapped:
        click.echo("Chanjo bootstrap successful! Now run: ")
        bed_path = root_path.joinpath(DEMO_BED_NAME if demo else BED_NAME[build])
        click.echo("chanjo --config {} link {}".format(conf_path, bed_path))
