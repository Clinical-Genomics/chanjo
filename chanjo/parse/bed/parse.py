# -*- coding: utf-8 -*-
"""Parse BED files including Sambamba output files."""
from chanjo.compat import zip
from chanjo.exc import BedFormattingError
from chanjo.utils import list_get


def chanjo(handle):
    """Parse the chanjo specific columns in a BED file.

    Args:
        handle (iterable): Chanjo-formatted BED lines

    Yields:
        dict: representation of row in BED file
    """
    lines = (line.strip() for line in handle if not line.startswith('#'))
    rows = (line.split('\t') for line in lines)
    for row in rows:
        yield expand_row(row)


def expand_row(row):
    """Parse a BED row.

    Args:
        List[str]: BED row

    Returns:
        dict: formatted BED row as a dict

    Raises:
        BedFormattingError: failure to parse first three columns
    """
    try:
        data = {
            'chrom': row[0],
            'chromStart': int(row[1]),
            'chromEnd': int(row[2])
        }
    except IndexError:
        raise BedFormattingError('make sure fields are tab-separated')
    except ValueError:
        raise BedFormattingError("positions malformatted: {}".format(row))

    try:
        data['score'] = int(list_get(row, 4))
    except ValueError:
        raise BedFormattingError('invalid BED syntax, score column is int')

    data['name'] = list_get(row, 3)
    data['strand'] = list_get(row, 5)
    element_combos = extra_fields(row[6:8])
    data['elements'] = element_combos
    data['extra_fields'] = row[8:]
    return data


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
