# -*- coding: utf-8 -*-
import itertools
import logging

from sqlalchemy.sql import func

from chanjo._compat import itervalues
from .core import Store
from .models import Exon, ExonStatistic, Gene, Sample, Transcript
from .utils import group_by_field, predict_gender

logger = logging.getLogger(__name__)


def filter_samples(query, group_id=None, sample_ids=None):
    """Filter a query to a subset of samples.

    Will return an unaltered query if none of the optional parameters
    are set. `group_id` takes precedence over `sample_ids`.

    Args:
        query (Query): SQLAlchemy query object
        group_id (Optional[str]): sample group identifier
        sample_ids (Optional[List[str]]): sample ids

    Returns:
        Query: filtered query object
    """
    if group_id:
        logger.debug('filter based on group')
        return query.filter(Sample.group == group_id)
    elif sample_ids:
        logger.debug('filter based on list of samples')
        return query.filter(Sample.sample_id.in_(sample_ids))
    else:
        return query


class ChanjoAPI(Store):

    """Interface to chanjo database for asking interesting questions.

    Attributes:
        weighten_average (BinaryExpression): weighter mean for metrics
    """

    def init_app(self, app, key_base='CHANJO_'):
        """Configure API (Flask style) after lazy initialization.

        Args:
            app (Flask): Flask app instance
            key_base (str): namespace to look for under ``app.config``

        Returns:
            ChanjoAPI: ``self``
        """
        uri = app.config["{}URI".format(key_base)]
        self.connect(db_uri=uri)
        return self

    @property
    def weighted_average(self):
        """Build a dynamic field to calculate a weighted average.

        Works for any of the exon metrics.

        Returns:
            BinaryExpression: dynamic field for a query
        """
        # length of the exon
        weight = Exon.end - Exon.start
        total_weight = func.sum(weight)
        total_value = func.sum(ExonStatistic.value * weight)
        weighted_mean = total_value / total_weight
        return weighted_mean

    def samples(self, group_id=None, sample_ids=None):
        """Get samples from the database.

        Args:
            group_id (Optional[str]): sample group identifier
            sample_ids (Optional[List[str]]): sample ids

        Returns:
            List[Sample]: samples objects from the database
        """
        query = self.query(Sample).order_by(Sample.sample_id)
        query = filter_samples(query, group_id=group_id, sample_ids=sample_ids)
        return query

    def mean(self, *samples):
        r"""Calculate mean values for all metrics on a per sample basis.

        Args:
            \*samples (Optional[List[str]]): filter by sample id

        Returns:
            dict: weighted averages grouped by sample
        """
        results = (self.query(Sample.sample_id, ExonStatistic.metric,
                              self.weighted_average)
                       .join(ExonStatistic.sample, ExonStatistic.exon)
                       .group_by(Sample.sample_id, ExonStatistic.metric))
        if samples:
            results = results.filter(Sample.sample_id.in_(samples))

        sample_groups = group_by_field(results, name='sample_id')
        return sample_groups

    def region(self, chromosome, start, end, sample_id=None, per=None):
        """Report coverage across a genomics region (of exons).

        Args:
            chromosome (str): chromosome id
            start (int): start position (inclusive)
            end (int): end position (inclusive)
            sample_id (Optional[str]): filter to only a single sample
            per (Optional[str]): report on a per exon basis ("exon")

        Returns:
            dict: weighted metrics (across samples)
        """
        results = (self.query(Exon.exon_id, ExonStatistic.metric,
                              self.weighted_average)
                       .join(ExonStatistic.exon)
                       .filter(Exon.chromosome == chromosome,
                               Exon.start >= start,
                               Exon.end <= end)
                       .group_by(ExonStatistic.metric))

        if sample_id:
            results = (results.join(ExonStatistic.sample)
                              .filter(Sample.sample_id == sample_id))

        if per == 'exon':
            results = results.group_by(Exon.exon_id)
            exon_groups = group_by_field(results, name='exon_id')
            return exon_groups
        else:
            data = {metric: value for exon_id, metric, value in results}
            return data

    def gene(self, *gene_ids):
        r"""Report aggregate statistics for particular genes.

        Args:
            \*gene_ids (List[str]): gene ids

        Returns:
            List[dict]: metrics grouped by sample and gene
        """
        samples = {}
        for gene_id in gene_ids:
            logger.debug('figure out which transcripts the gene belongs to')
            tx_ids = list(self.gene_to_transcripts(gene_id))
            if len(tx_ids) == 0:
                raise AttributeError("gene id not in database: {}"
                                     .format(gene_id))

            results = self.transcript_to_exons(*tx_ids)
            for data in group_by_field(results, name='sample_id'):
                if data['sample_id'] not in samples:
                    samples[data['sample_id']] = {'sample_id': data['sample_id']}
                samples[data['sample_id']][gene_id] = data

        return itervalues(samples)

    def transcripts(self, *transcript_ids):
        r"""Report metrics on specific transcripts.

        Args:
            \*transcript_ids (List[str]): transcript ids

        Returns:
            List[tuple]: sample, transcript, metric, value
        """
        results = (self.query(Sample.sample_id,
                              Transcript.transcript_id,
                              ExonStatistic.metric,
                              self.weighted_average)
                       .join(ExonStatistic.sample, ExonStatistic.exon,
                             Exon.transcripts)
                       .filter(Transcript.transcript_id.in_(transcript_ids))
                       .group_by(Sample.sample_id, ExonStatistic.metric,
                                 Transcript.transcript_id))
        return results

    def all_transcripts(self, sample_id, *gene_ids):
        r"""Fetch all transcripts from the database.

        Args:
            sample_id (str): restrict query to a sample id
            \*gene_ids (List[str]): genes to convert to transcripts

        Returns:
            List[Transcript]: transcript models related to the genes
        """
        query = (self.query(Transcript)
                     .join(Transcript.exons, Exon.stats, ExonStatistic.sample)
                     .filter(Sample.sample_id == sample_id))
        if gene_ids:
            tx_ids = self.gene_to_transcripts(*gene_ids)
            query = query.filter(Transcript.transcript_id.in_(tx_ids))
        return query

    def transcripts_to_genes(self, transcript_ids, db_ids=False):
        """Fetch a list of genes related to some exons.

        Args:
            transcript_ids (List[str]): transcript ids to convert to genes
            db_ids (Optional[bool]): if sending in primary key ids

        Returns:
            List[Gene]: gene models related to the transcripts
        """
        results = self.query(Gene).join(Gene.transcripts)
        if db_ids:
            results = results.filter(Transcript.id.in_(transcript_ids))
        else:
            condition = Transcript.transcript_id.in_(transcript_ids)
            results = results.filter(condition)
        return results

    def exons_to_transcripts(self, exons_ids, db_ids=False):
        """Fetch a list of transcripts related to some exons.

        Args:
            exon_ids (List[str]): list of exon ids
            db_ids (Optional[bool]): if sending in primary key ids

        Returns:
            List[Transcript]: transcripts related to the exons
        """
        results = self.query(Transcript).join(Transcript.exons)
        if db_ids:
            results = results.filter(Exon.id.in_(exons_ids))
        else:
            results = results.filter(Exon.exon_id.in_(exons_ids))
        return results

    def incomplete_exons(self, level=10, threshold=100, group_id=None,
                         sample_ids=None):
        """Fetch exons with incomplete coverage at a specifc level.

        Args:
            level (Optional[int]): completeness level, default: 10
            threshold (Optional[int]): % completeness cutoff, default: 100
            group_id (Optional[str]): sample group identifier
            sample_ids (Optional[List[str]]): sample ids

        Returns:
            List[tuple]: sample, exon, completeness value
        """
        completeness = "completeness_{}".format(level)
        query = (self.query(Sample.sample_id,
                            Exon.exon_id,
                            ExonStatistic.value)
                     .join(ExonStatistic.exon, ExonStatistic.sample)
                     .filter(ExonStatistic.metric == completeness,
                             ExonStatistic.value < threshold))
        query = filter_samples(query, group_id=group_id, sample_ids=sample_ids)
        return query

    def gene_panel(self, gene_ids, group_id=None, sample_ids=None):
        """Report metrics for a panel of genes.

        Args:
            gene_ids (List[str]): gene ids for the panel
            group_id (Optional[str]): sample group identifier
            sample_ids (Optional[List[str]]): sample ids

        Returns:
            List[tuple]: sample, metric, weighted average value
        """
        tx_ids = list(self.gene_to_transcripts(*gene_ids))
        query = self.transcript_to_exons(*tx_ids)
        query = filter_samples(query, group_id=group_id, sample_ids=sample_ids)
        return query

    def transcript_to_exons(self, *transcript_ids):
        """Fetch a unique list of exons related to some transcripts.

        Args:
            transcript_ids (List[str]): transcript ids to look up

        Returns:
            List[tuple]: sample, metric, weighted average value
        """
        results = (self.query(Sample.sample_id, ExonStatistic.metric,
                              self.weighted_average)
                       .join(ExonStatistic.sample, ExonStatistic.exon,
                             Exon.transcripts)
                       .filter(Transcript.transcript_id.in_(transcript_ids))
                       .group_by(Sample.sample_id, ExonStatistic.metric))
        return results

    def gene_to_transcripts(self, *gene_ids):
        r"""Fetch a unique list of transcripts related to some genes.

        Args:
            \*gene_ids (List[str]): gene ids

        Returns:
            List[str]: transcript ids
        """
        results = (self.query(Transcript.transcript_id)
                       .join(Transcript.gene)
                       .filter(Gene.gene_id.in_(gene_ids)))
        return (result[0] for result in results)

    def sex_coverage(self, sex_chromosomes=('X', 'Y')):
        """Query for average on X/Y chromsomes.

        Args:
            sex_chromosomes (Optional[tuple]): chromosome ids

        Returns:
            List[tuple]: sample, chromosome, weighted average coverage
        """
        query = (self.query(Sample.sample_id,
                            Exon.chromosome,
                            self.weighted_average)
                     .join(ExonStatistic.exon, ExonStatistic.sample)
                     .filter(Exon.chromosome.in_(sex_chromosomes),
                             ExonStatistic.metric == 'mean_coverage')
                     .group_by(Sample.sample_id, Exon.chromosome))
        return query

    def sex_check(self, group_id=None, sample_ids=None):
        """Predict gender based on coverage of sex chromosomes.

        Args:
            group_id (Optional[str]): sample group identifier
            sample_ids (Optional[List[str]]): sample ids

        Returns:
            tuple: sample, gender, coverage X, coverage, Y
        """
        query = self.sex_coverage()
        query = filter_samples(query, group_id=group_id, sample_ids=sample_ids)
        logger.debug('group rows based on sample')
        samples = itertools.groupby(query, lambda row: row[0])
        for sample_id, chromosomes in samples:
            sex_coverage = [coverage for _, _, coverage in chromosomes]
            logger.debug('predict gender')
            # run the predictor
            gender = predict_gender(*sex_coverage)
            yield sample_id, gender, sex_coverage[0], sex_coverage[1]
