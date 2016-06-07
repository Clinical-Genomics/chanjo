# -*- coding: utf-8 -*-
import codecs
import logging

import click
from path import path
import yaml
from distutils.spawn import find_executable

from .bootstrap import pull, DB_NAME
from .demo import setup_demo

log = logging.getLogger(__name__)


@click.command()
@click.option('-f', '--force', is_flag=True, help='overwrite existing files')
@click.option('-d', '--demo', is_flag=True, help='copy demo files')
@click.argument('root_dir', default='.', required=False)
@click.pass_context
def init(context, force, demo, root_dir):
    """Bootstrap a new chanjo setup."""
    # test setup of sambamba
    sambamba_bin = find_executable('sambamba')
    if sambamba_bin is None:  # pragma: no cover
        log.warn("'sambamba' command not found")
    else:
        log.debug("'sambamba' found: %s", sambamba_bin)

    root_path = path(root_dir)
    log.info("setting up chanjo under: %s", root_path.abspath())

    if demo:
        log.info("copying demo files: %s", root_dir)
        setup_demo(root_dir, force=force)
        abs_db_path = root_path.joinpath('coverage.sqlite3').abspath()
        db_uri = "sqlite:///{}".format(abs_db_path)
        # inquire about bootstrapping
    elif click.confirm('Bootstrap CCDS transcript database?'):
        # ensure root dir exists
        root_path.makedirs_p()
        pull(root_dir, force=force)
        abs_db_path = root_path.joinpath(DB_NAME).abspath()
        db_uri = "sqlite:///{}".format(abs_db_path)
    else:
        db_uri = click.prompt('Please enter database to use?')

    # setup config file
    conf_path = root_path.joinpath('chanjo.yaml')
    with codecs.open(conf_path, 'w', encoding='utf-8') as conf_handle:
        data = {'database': db_uri}
        data_str = yaml.dump(data, default_flow_style=False)
        log.info("writing config file: %s", conf_path)
        conf_handle.write(data_str)
