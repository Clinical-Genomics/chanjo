#!/usr/bin/env python
from chanjo.compat import text_type
from chanjo.utils import id_generator


def test_id_generator():
    """Test generating a random id."""
    # difficult to test randomly generated strings...
    assert len(id_generator()) == 8
    assert isinstance(id_generator(), text_type)

    # test with custom sized id
    assert len(id_generator(3)) == 3

    # test edge case with 0 lenght
    assert id_generator(0) == ''
