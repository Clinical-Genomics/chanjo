# -*- coding: utf-8 -*-
import click
from click.termui import echo, style

import chanjo
from chanjo.config import questionnaire


@click.command()
@click.option('-s', '--setup', is_flag=True, help='setup database tables')
@click.pass_context
def init(context, setup):
    """Walk user through setting up a new config file."""
    # print a nice welcome message
    click.echo(chanjo.__banner__)

    questions = [('annotate.cutoff', 'sufficient coverage',
                  context.obj.get('annotate', {}).get('cutoff', 10)),
                 ('dialect', 'preferred SQL-dialect',
                  context.parent.db.dialect),
                 ('db', 'central database path/URI', context.parent.db.uri)]
    # launch init pipeline
    init_pipeline('chanjo', context.obj, questions)

    if setup:
        context.parent.db.uri = context.obj['db']
        context.parent.db.set_up()


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

    # Write to the config file
    config.save(default_flow_style=False)
