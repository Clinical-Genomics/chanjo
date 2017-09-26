# -*- coding: utf-8 -*-
import codecs
from distutils.spawn import find_executable
import logging

import click
from path import Path
import ruamel.yaml

from chanjo.store.api import ChanjoDB
from chanjo.init.bootstrap import pull, BED_NAME, DB_NAME
from chanjo.init.demo import setup_demo, DEMO_BED_NAME

LOG = logging.getLogger(__name__)


@click.command()
@click.option('-f', '--force', is_flag=True, help='overwrite existing files')
@click.option('-d', '--demo', is_flag=True, help='copy demo files')
@click.option('-a', '--auto', is_flag=True)
@click.argument('root_dir', default='.', required=False)
@click.pass_context
def init(context, force, demo, auto, root_dir):
    """Bootstrap a new chanjo setup."""
    is_bootstrapped = False
    root_path = Path(root_dir)

    LOG.info("setting up chanjo under: %s", root_path)
    db_uri = context.obj.get('database')
    db_uri = db_uri or "sqlite:///{}".format(root_path.joinpath(DB_NAME).abspath())

    # test setup of sambamba
    sambamba_bin = find_executable('sambamba')
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
    elif auto or click.confirm('Bootstrap HGNC transcript BED?'):
        pull(root_dir, force=force)

        LOG.info("configure new chanjo database: %s", db_uri)
        chanjo_db = ChanjoDB(db_uri)
        chanjo_db.set_up()
        is_bootstrapped = True

    # setup config file
    root_path.makedirs_p()
    conf_path = root_path.joinpath('chanjo.yaml')
    with codecs.open(conf_path, 'w', encoding='utf-8') as conf_handle:
        data = {'database': db_uri}
        data_str = ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper)
        LOG.info("writing config file: %s", conf_path)
        conf_handle.write(data_str)

    if is_bootstrapped:
        click.echo('Chanjo bootstrap successful! Now run: ')
        bed_path = root_path.joinpath(DEMO_BED_NAME if demo else BED_NAME)
        click.echo("chanjo --config {} link {}".format(conf_path, bed_path))
