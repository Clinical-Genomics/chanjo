# -*- coding: utf-8 -*-
from __future__ import division
from collections import namedtuple

from chanjo.store.models import TranscriptStat, Sample, Exon
from .parse import sambamba
from .utils import groupby_tx

Result = namedtuple('Result', ['models', 'count', 'sample'])


def load_transcripts(sequence, sample_id=None, group_id=None, source=None, threshold=None):
    """Process a sequence of exon lines.

    Args:
        sequence (sequence): list of chanjo bed lines
        sample_id (Optional[str]): unique sample id, else auto-guessed
        grouip_id (Optional[str]): id to group samples
        source (Optional[str]): path to coverage source (BAM/Sambamba)
        threshold (Optional[int]): completeness level to disqualify exons

    Returns:
        Result: iterators of `Transcript`, transcripts processed, sample model
    """
    exons = sambamba.depth_output(sequence)
    transcripts = groupby_tx(exons, sambamba=True)
    raw_stats = ((tx_id, tx_stat(tx_id, exons, threshold=threshold))
                 for tx_id, exons in transcripts.items())

    if sample_id is None:
        sample_id = next(iter(transcripts.values()))[0]['sampleName']
    sample_obj = Sample(id=sample_id, group_id=group_id, source=source)

    models = (make_model(sample_obj, tx_id, raw_stat) for tx_id, raw_stat
              in raw_stats)
    return Result(models=models, count=len(transcripts), sample=sample_obj)


def tx_stat(transcript_id, exons, threshold=None):
    """Calculate metrics for transcript stats model.

    Args:
        transcript_id (str): unqiue transcript id
        exons (List[dict]): list of exon transcripts
        threshold (Optional[int]): completeness level to disqualify exons

    Returns:
        dict: aggregated stats over all exons
    """
    sums = {'bases': 0, 'mean_coverage': 0}
    incomplete_exons = []

    # for each of the exons (linked to one transcript)
    for exon in exons:
        # go over each of the fields to sum up
        exon_length = (exon['chromEnd'] - exon['chromStart'])
        sums['bases'] += exon_length
        sums['mean_coverage'] += (exon['meanCoverage'] * exon_length)

        # add to the total sum for completeness levels
        for comp_key in [10, 15, 20, 50, 100]:
            if comp_key in exon['thresholds']:
                sums_key = "completeness_{}".format(comp_key)
                if sums_key not in sums:
                    sums[sums_key] = 0
                completeness = exon['thresholds'][comp_key]
                sums[sums_key] += (completeness * exon_length)

                if threshold == comp_key and completeness < 100:
                    exon_obj = Exon(exon['chrom'], exon['chromStart'],
                                    exon['chromEnd'], completeness)
                    incomplete_exons.append(exon_obj)

    fields = {key: (value / sums['bases']) for key, value in sums.items() if key != 'bases'}
    fields['incomplete_exons'] = incomplete_exons
    fields['threshold'] = threshold
    return fields


def make_model(sample_obj, transcript_id, fields):
    """Compose a transcript stat model from fields.

    Args:
        sample_obj (Sample): Sample database model
        transcript_id (str): unique transcript id
        fields (dict): key/values of metrics

    Returns:
        Transcript: composed transcript model
    """
    tx_model = TranscriptStat(sample_id=sample_obj.id, transcript_id=transcript_id, **fields)
    return tx_model
