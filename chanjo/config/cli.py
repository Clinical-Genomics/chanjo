# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import click

from .core import init_pipeline
from .. import __banner__


@click.command()
@click.option('-r', '--remove', is_flag=True, help='remove config option')
@click.argument('key')
@click.argument('value', required=False)
@click.pass_context
def config(context, key, value, remove):
  """Only handles string values."""
  # update or delete the config key-value pair
  # the key can be provide as a path to nested commands: "user.name"
  if remove:
    context.obj.unset(key, scope=context.obj.user_data)

  else:
    if value is None:
      click.echo(context.obj.get(key))

    if value.isnumeric():
      value = int(value)

    context.obj.set(key, value, scope=context.obj.user_data)

  # persist updates to the config file
  context.obj.save()


@click.command()
@click.pass_context
def init(context):
  """Walk user through setting up a new config file."""
  # print a nice welcome message
  click.echo(__banner__)

  questions = [
    ('annotate.cutoff', 'sufficient coverage',
      context.obj.get('annotate', {}).get('cutoff', 10)),
    ('dialect', 'preferred SQL-dialect', context.parent.db.dialect),
    ('db', 'central database path/URI', context.parent.db.uri)
  ]

  # launch init pipeline
  init_pipeline('chanjo', context.obj, questions)
