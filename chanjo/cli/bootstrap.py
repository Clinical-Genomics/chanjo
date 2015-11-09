# -*- coding: utf-8 -*-
import logging
import os

import click
from path import path

from chanjo import bootstrap as bootstrap_api
from .init import init

logger = logging.getLogger(__name__)


@click.command()
@click.option('-f', '--force', is_flag=True)
@click.argument('directory', default='./coverage', required=False)
@click.pass_context
def bootstrap(context, force, directory):
    """Link related genomic elements."""
    bootstrap_api.pull(directory, force=force)

    config_path = os.path.join(directory, 'chanjo.yaml')
    context.obj.config_path = path(config_path)
    context.invoke(init, automate=True)
