# -*- coding: utf-8 -*-
import click
from click.termui import echo, style

import chanjo
from chanjo.config import questionnaire
from chanjo.store import Store


@click.command()
@click.option('-s', '--setup', is_flag=True, help='setup database tables')
@click.option('-r', '--reset', is_flag=True, help='reset an existing database')
@click.option('-a', '--automate', is_flag=True, help='run non-interactively')
@click.pass_context
def init(context, setup, reset, automate):
    """Walk user through setting up a new config file."""
    # print a nice welcome message
    click.echo(chanjo.__banner__)

    if not automate:
        questions = [('sambamba.cov_treshold', 'sufficient coverage',
                      context.obj.get('sambamba', {}).get('cov_treshold',
                                                          [10, 20])),
                     ('database', 'central database path/URI',
                      context.obj['database'])]
        # launch init pipeline
        init_pipeline('chanjo', context.obj, questions)

    if setup:
        chanjo_db = Store(uri=context.obj.user_data['database'])
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

    # write to the config file
    config.save(default_flow_style=False)
