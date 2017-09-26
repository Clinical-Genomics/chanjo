# -*- coding: utf-8 -*-
import codecs
from distutils.spawn import find_executable
import logging
import gzip

import click
from path import Path
import ruamel.yaml
from sqlalchemy.exc import IntegrityError

from chanjo.store.api import ChanjoDB
from chanjo.load.link import link_elements
from chanjo.resources import BED_NAME
from chanjo.init.demo import setup_demo, DEMO_BED_NAME

DB_NAME = 'chanjo.coverage.sqlite3'

LOG = logging.getLogger(__name__)


@click.command()
@click.option('-f', '--force', is_flag=True, help='overwrite existing files')
@click.option('-d', '--demo', is_flag=True, help='copy demo files')
@click.option('-e', '--exons', type=click.Path(exists=True),
    help='Specify a bed file with exon information'
)
@click.argument('root_dir', default='.', required=False)
@click.pass_context
def init(context, force, demo, exons, root_dir):
    """Setup a new chanjo database."""
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
        try:
            setup_demo(root_dir, force=force)
        except FileExistsError as err:
            context.abort()
        # Set the exons path
        exons = root_path.joinpath(DEMO_BED_NAME)

    if not exons:
        exons = BED_NAME

    LOG.info("configure new chanjo database: %s", db_uri)
    chanjo_db = ChanjoDB(db_uri)
    chanjo_db.set_up()

    # setup config file
    root_path.makedirs_p()
    conf_path = root_path.joinpath('chanjo.yaml')
    with codecs.open(conf_path, 'w', encoding='utf-8') as conf_handle:
        data = {'database': db_uri}
        data_str = ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper)
        LOG.info("writing config file: %s", conf_path)
        conf_handle.write(data_str)
    
    LOG.info("Linking transcripts from file: %s", exons)
    if exons.endswith('.gz'):
        bed_stream = gzip.open(exons, mode='rt')
    else:
        bed_stream = codecs.open(exons, 'r')

    result = link_elements(bed_stream)
    with click.progressbar(result.models, length=result.count,
                           label='adding transcripts') as bar:
        for tx_model in bar:
            chanjo_db.add(tx_model)
    try:
        chanjo_db.save()
    except IntegrityError:
        LOG.exception('elements already linked?')
        chanjo_db.session.rollback()
        click.echo("use 'chanjo db setup --reset' to re-build")
        context.abort()

