# -*- coding: utf-8 -*-
import logging

import click
from click.termui import echo, style

import chanjo
from chanjo.compat import iteritems
from chanjo.config import questionnaire
from chanjo.store import Store
from chanjo.store.models import BASE
from chanjo.store.txmodels import BASE as TXBASE

logger = logging.getLogger(__name__)


@click.command()
@click.option('-s', '--setup', is_flag=True, help='setup database tables')
@click.option('-r', '--reset', is_flag=True, help='reset an existing database')
@click.option('-a', '--automate', is_flag=True, help='run non-interactively')
@click.option('-t', '--transcripts', is_flag=True,
              help='focus only on transcripts on the database level')
@click.pass_context
def init(context, setup, reset, automate, transcripts):
    """Walk user through setting up a new config file."""
    # print a nice welcome message
    click.echo(chanjo.__banner__)

    cov_tresholds = (context.obj.get('sambamba', {})
                                .get('cov_treshold', [10, 20]))
    defaults = {'sambamba.cov_treshold': {'value': cov_tresholds,
                                          'prompt': 'sufficient coverage'},
                'database': {'value': str(context.obj['database']),
                             'prompt': 'central database path/URI'}}

    if not automate:
        questions = [(key, value['prompt'], value['value'])
                     for key, value in iteritems(defaults)]
        # launch init pipeline
        init_pipeline('chanjo', context.obj, questions)
    else:
        logger.info('setting default config values')
        for key, value in iteritems(defaults):
            context.obj.set(key, value['value'], scope=context.obj.user_data)

    # write to the config file
    context.obj.save(default_flow_style=False)

    if setup:
        only_tx = transcripts or context.obj.get('transcripts') or False
        base = TXBASE if only_tx else BASE
        chanjo_db = Store(uri=context.obj['database'], base=base)
        if reset:
            chanjo_db.tear_down()
        chanjo_db.set_up()


def init_pipeline(program, config, questions):
    """Initializes a config object by interactively asking questions."""
    if config.user_data:
        # Some existing user settings were found, warn about overwriting them
        message = "{program} {note}\tThe existing {file} will be updated"
        segments = dict(program=program, note=style('existing', fg='yellow'),
                        file=style(config.config_path.basename(), fg='white'))
        echo(message.format(**segments))

    # Launch questionnaire
    user_defaults = questionnaire(questions)
    # Set the selected user defaults
    for dot_key, value in user_defaults.items():
        config.set(dot_key, value, scope=config.user_data)
