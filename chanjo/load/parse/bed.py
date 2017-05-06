# -*- coding: utf-8 -*-
"""Parse BED files including Sambamba output files."""
from chanjo.exc import BedFormattingError


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

    data['name'] = list_get(row, 3)
    element_combos = extra_fields(row[4:7])
    data['elements'] = element_combos
    data['extra_fields'] = row[7:]
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
        symbols = columns[2].split(',')
    except IndexError:
        return []
    return zip(transcripts, genes, symbols)


def list_get(list_obj, index, default=None):
    """Like ``.get`` for list object.

    Args:
        list_obj (list): list to look up an index in
        index (int): index position to look up
        default (Optional[object]): default return value. Defaults to None.

    Returns:
        object: any object found at the index or ``default``
    """
    try:
        return list_obj[index]
    except IndexError:
        return default
