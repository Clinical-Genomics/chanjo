# -*- coding: utf-8 -*-
"""Parse BED files including Sambamba output files."""
from chanjo._compat import zip
from chanjo.sambamba import parse


def chanjo(handle):
    """Parse a general BED file."""
    row_data = parse.depth_output(handle)
    for data in row_data:
        data['name'] = data['extraFields'][0]
        data['score'] = int(data['extraFields'][1])
        data['strand'] = data['extraFields'][2]
        data['elements'] = extra_fields(data['extraFields'][3:])
        yield data


def extra_fields(columns):
    """Parse additional, chanjo specific fields."""
    transcripts = columns[0].split(',')
    genes = columns[1].split(',')
    return zip(transcripts, genes)
