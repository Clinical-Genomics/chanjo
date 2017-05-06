# -*- coding: utf-8 -*-
"""
Parse the sambamba "depth region" output.
"""
from chanjo.exc import BedFormattingError


def depth_output(handle):
    """Parse the output.

    Args:
        handle (iterable): Chanjo-formatted BED lines

    Yields:
        dict: parsed sambamba output row

    Raises:
        BedFormattingError: if the BED file doesn't contain enough columns
    """
    lines = (line.strip() for line in handle)
    rows = (line.split('\t') for line in lines)
    # expect only a single header row
    header_row = next(rows)
    if len(header_row) < 6:
        raise BedFormattingError('make sure fields are tab-separated')
    header_data = expand_header(header_row)
    # parse rows
    for row in rows:
        yield expand_row(header_data, row)


def expand_header(row):
    """Parse the header information.

    Args:
        List[str]: sambamba BED header row

    Returns:
        dict: name/index combos for fields
    """
    # figure out where the sambamba output begins
    sambamba_start = row.index('readCount')
    sambamba_end = row.index('sampleName')
    coverage_columns = row[sambamba_start + 2:sambamba_end]
    thresholds = {int(column.replace('percentage', '')): row.index(column)
                  for column in coverage_columns}
    keys = {
        'readCount': sambamba_start,
        'meanCoverage': sambamba_start + 1,
        'thresholds': thresholds,
        'sampleName': sambamba_end,
        'extraFields': slice(3, sambamba_start)
    }
    return keys


def expand_row(header, row):
    """Parse information in row to dict.

    Args:
        header (dict): key/index header dict
        row (List[str]): sambamba BED row

    Returns:
        dict: parsed sambamba output row
    """
    thresholds = {threshold: float(row[key])
                  for threshold, key in header['thresholds'].items()}
    data = {
        'chrom': row[0],
        'chromStart': int(row[1]),
        'chromEnd': int(row[2]),
        'sampleName': row[header['sampleName']],
        'readCount': int(row[header['readCount']]),
        'meanCoverage': float(row[header['meanCoverage']]),
        'thresholds': thresholds,
        'extraFields': row[header['extraFields']]
    }
    return data
