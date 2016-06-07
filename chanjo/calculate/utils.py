# -*- coding: utf-8 -*-
import json


def dump_json(data, pretty=False):
    """Print JSON to console."""
    if pretty:
        json_args = dict(indent=4, sort_keys=True)
    else:
        json_args = {}
    return json.dumps(data, **json_args)
