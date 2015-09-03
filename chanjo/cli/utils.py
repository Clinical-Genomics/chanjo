# -*- coding: utf-8 -*-
import json

import click


def dump_json(*items):
    """Dump list of dicts as json objects.

    Args:
        items (List[dict]): list of JSON serializable dicts
    """
    for item in items:
        json_dump = json.dumps(item)
        click.echo(json_dump)
