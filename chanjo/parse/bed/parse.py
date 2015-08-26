# -*- coding: utf-8 -*-
"""Parse BED files including Sambamba output files."""
from chanjo._compat import zip
from chanjo.parse import sambamba
from chanjo.utils import list_get


def chanjo(handle):
    """Parse a general BED file.

    Parses the optional columns not covered by Sambamba.

    Args:
        handle (iterable): Chanjo-formatted BED lines

    Yields:
        dict: representation of row in BED file
    """
    row_data = sambamba.depth_output(handle)
    for data in row_data:
        data['name'] = list_get(data['extraFields'], 0)
        data['score'] = int(list_get(data['extraFields'], 1, default=0))
        data['strand'] = list_get(data['extraFields'], 2)
        element_combos = extra_fields(data['extraFields'][3:])
        data['elements'] = element_combos
        yield data


def extra_fields(columns):
    """Parse additional, chanjo specific fields.

    Contains transcript and gene ids.

    Args:
        columns (List[str]): list of two columns with related element ids

    Returns:
        List[tuple]: list of tuples with paired elements
    """
    try:
        transcripts = columns[0].split(',')
        genes = columns[1].split(',')
    except IndexError:
        return []
    return zip(transcripts, genes)
