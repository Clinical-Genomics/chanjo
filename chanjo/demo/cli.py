# -*- coding: utf-8 -*-
from pkg_resources import resource_filename, resource_listdir

import click
from path import path


@click.command()
@click.argument('location', type=click.Path(), default='./chanjo-demo',
                required=False)
@click.pass_context
def demo(context, location):
    """Copy demo files to a directory.

    \b
    LOCATION: directory to add demofiles to (default: ./chanjo-demo)
    """
    user_dir = path(location)
    pkg_dir = __name__.rpartition('.')[0]
    demo_dir = path(resource_filename(pkg_dir, 'files'))

    # make sure we don't overwrite exiting files
    for demo_file in resource_listdir(pkg_dir, 'files'):
        user_file_path = user_dir.joinpath(demo_file)
        if user_file_path.exists():
            click.echo("{} exists, pick a different location"
                       .format(user_file_path))
            context.abort()

    try:
        # we can copy the directory(tree)
        demo_dir.copytree(user_dir)
    except OSError:
        click.echo('The location must be a non-existing directory.')
        context.abort()

    # inform the user
    click.echo("Successfully copied demo files to {}".format(user_dir))
