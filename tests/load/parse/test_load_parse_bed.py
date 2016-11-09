# -*- coding: utf-8 -*-
import pytest

from chanjo.load.parse import bed
from chanjo.exc import BedFormattingError


def test_expand_row(bed_row):
    data = bed.expand_row(bed_row)
    assert data['name'] == bed_row[3]

    # test with malformatted values
    # GIVEN position is not int
    bed_row[1] = 'paulthomas'
    with pytest.raises(BedFormattingError):
        bed.expand_row(bed_row)


def test_expand_row_space_separated():
    with pytest.raises(BedFormattingError):
        bed.expand_row(['22 32588888 32589173 22-32588888-32589173'])


def test_chanjo(bed_lines):
    exons = list(bed.chanjo(bed_lines))
    assert len(exons) == 19
    exon = exons[0]
    assert exon['chrom'] == '1'
    assert exon['name'] == '1-11-18'


def test_extra_fields():
    # GIVEN no extra columns
    extra_cols = []
    data = bed.extra_fields(extra_cols)
    assert data == []


def test_list_get():
    # GIVEN a regular list with three items
    reg_list = [1, 2, 3]
    # WHEN accsesing existing 2nd item
    item = bed.list_get(reg_list, 1)
    # THEN it should return the list item
    assert item == reg_list[1]

    # WHEN accessing non-existing 4th item
    item = bed.list_get(reg_list, 3)
    # THEN it should return None
    assert item is None

    # WHEN accessing existing item with default
    item = bed.list_get(reg_list, 2, default=10)
    # THEN it should return the item
    assert item == reg_list[2]

    # WHEN accessing non-existing item with default
    default = 10
    item = bed.list_get(reg_list, 4, default=default)
    # THEN it should return the default
    assert item == default

    # GIVEN empty list
    empty_list = []
    # WHEN accessing any item
    item = bed.list_get(empty_list, 0)
    # THEN it should always be None
    assert item is None
