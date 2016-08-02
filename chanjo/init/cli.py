# -*- coding: utf-8 -*-
import codecs
import logging

import click
from path import path
import yaml
from distutils.spawn import find_executable

from chanjo.store.api import ChanjoDB
from .bootstrap import pull, BED_NAME, DB_NAME
from .demo import setup_demo

log = logging.getLogger(__name__)


@click.command()
@click.option('-f', '--force', is_flag=True, help='overwrite existing files')
@click.option('-d', '--demo', is_flag=True, help='copy demo files')
@click.option('-a', '--auto', is_flag=True)
@click.argument('root_dir', default='.', required=False)
@click.pass_context
def init(context, force, demo, auto, root_dir):
    """Bootstrap a new chanjo setup."""
    root_path = path(root_dir).abspath()
    log.info("setting up chanjo under: %s", root_path)
    db_uri = context.obj.get('database')
    abs_db_path = root_path.joinpath(DB_NAME)
    db_uri = db_uri or "sqlite:///{}".format(abs_db_path)
    # test setup of sambamba
    sambamba_bin = find_executable('sambamba')
    if sambamba_bin is None:  # pragma: no cover
        log.warn("'sambamba' command not found")
    else:
        log.debug("'sambamba' found: %s", sambamba_bin)

    if demo:
        log.info("copying demo files: %s", root_dir)
        setup_demo(root_dir, force=force)
    elif auto or click.confirm('Bootstrap CCDS transcript BED?'):
        # ensure root dir exists
        root_path.makedirs_p()
        pull(root_dir, force=force)

        log.info("configure new chanjo database: %s", db_uri)
        chanjo_db = ChanjoDB(db_uri)
        chanjo_db.set_up()

    # setup config file
    conf_path = root_path.joinpath('chanjo.yaml')
    with codecs.open(conf_path, 'w', encoding='utf-8') as conf_handle:
        data = {'database': db_uri}
        data_str = yaml.dump(data, default_flow_style=False)
        log.info("writing config file: %s", conf_path)
        conf_handle.write(data_str)

    click.echo('Chanjo bootstrap successful! Now run: ')
    bed_path = root_path.joinpath(BED_NAME)
    click.echo("chanjo --config {} link {}".format(conf_path, bed_path))
