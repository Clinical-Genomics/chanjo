# -*- coding: utf-8 -*-
import click

from .core import init_pipeline
from .. import __banner__


@click.command()
@click.pass_context
def init(context):
    """Walk user through setting up a new config file."""
    # print a nice welcome message
    click.echo(__banner__)

    questions = [('annotate.cutoff', 'sufficient coverage',
                  context.obj.get('annotate', {}).get('cutoff', 10)),
                 ('dialect', 'preferred SQL-dialect',
                  context.parent.db.dialect),
                 ('db', 'central database path/URI', context.parent.db.uri)]

    # launch init pipeline
    init_pipeline('chanjo', context.obj, questions)
