# -*- coding: utf-8 -*-
from chanjo.calculate import utils


def test_dump_json():
    # GIVEN some dict
    data = {'name': 'PT Anderson', 'age': 45}
    # WHEN dumping to JSON with pretty-option enabled
    json = utils.dump_json(data, pretty=True)
    # THEN the output is formatted over multiple lines
    assert isinstance(json, str)
    assert len(json.split('\n')) == 4
