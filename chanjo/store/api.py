# -*- coding: utf-8 -*-
from __future__ import division
import itertools
import logging

from sqlalchemy.sql import func

from chanjo.compat import itervalues
from chanjo.utils import list_get
from .core import Store
from .converter import ChanjoConverterMixin
from .models import Exon, ExonStatistic, Sample, Transcript
from .utils import filter_samples, group_by_field, predict_gender

logger = logging.getLogger(__name__)


class ChanjoAPI(Store, ChanjoConverterMixin):

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
        weighted_mean = (total_value / total_weight).label('weighted_mean')
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

    def means(self, query=None):
        """Calculate means on a per sample basis.

        Args:
            query (Optional[Query]): initialized and filtered query

        Returns:
            List[tuple]: sample id and grouped mean metrics
        """
        query = query or self.query()
        ready_query = (query.add_columns(Sample.sample_id,
                                         ExonStatistic.metric,
                                         self.weighted_average)
                            .join(ExonStatistic.sample, ExonStatistic.exon)
                            .group_by(Sample.sample_id, ExonStatistic.metric)
                            .order_by(Sample.sample_id))
        results = group_by_field(ready_query)
        return results

    def region_alt(self, region_id, sample_id=None, per=None):
        """Parse region id as input for `region` method.

        Args:
            region_id (str): for example 1:1242314-1243419
            sample_id (Optional[str]): filter to only a single sample
            per (Optional[str]): report on a per exon basis ("exon")

        Returns:
            dict: weighted metrics (across samples)
        """
        try:
            chromosome, pos_str = region_id.split(':')
        except ValueError:
            raise ValueError("unsupported region id: {}".format(region_id))
        start, end = [int(pos) for pos in pos_str.split('-')]
        data = self.region(chromosome, start, end, sample_id=sample_id,
                           per=per)
        return data

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
                       .group_by(ExonStatistic.metric)
                       .order_by(Exon.exon_id))

        if sample_id:
            results = (results.join(ExonStatistic.sample)
                              .filter(Sample.sample_id == sample_id))

        if per == 'exon':
            results = results.group_by(Exon.exon_id)
            exon_groups = group_by_field(results)
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
            exon_objs = self.gene_exons(gene_id).all()
            if len(exon_objs) == 0:
                raise AttributeError("gene id not in database: {}"
                                     .format(gene_id))
            exon_ids = [exon_obj.exon_id for exon_obj in exon_objs]
            query = (self.query().filter(Exon.exon_id.in_(exon_ids)))
            for sample_id, data in self.means(query):
                if sample_id not in samples:
                    samples[sample_id] = {'sample_id': sample_id, 'genes': {}}
                samples[sample_id]['genes'][gene_id] = data

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

    def incomplete_exons(self, query=None, level=10, threshold=100):
        """Fetch exons with incomplete coverage at a specifc level.

        Args:
            level (Optional[int]): completeness level, default: 10
            threshold (Optional[int]): % completeness cutoff, default: 100
            group_id (Optional[str]): sample group identifier
            sample_ids (Optional[List[str]]): sample ids

        Returns:
            List[tuple]: sample_id, dict with exons and completeness
        """
        completeness = "completeness_{}".format(level)
        query = query or self.query()
        ready_query = (self.query(Sample.sample_id,
                                  Exon.exon_id,
                                  ExonStatistic.value)
                           .join(ExonStatistic.exon, ExonStatistic.sample)
                           .filter(ExonStatistic.metric == completeness,
                                   ExonStatistic.value < threshold)
                           .order_by(Sample.sample_id))
        exon_samples = group_by_field(ready_query)
        return exon_samples

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

    def diagnostic_yield(self, sample_id, exon_ids=None, query=None, level=10,
                         threshold=100):
        """Calculate transcripts that aren't completely covered.

        This metric only applies to one sample in isolation. Otherwise
        it's hard to know what to do with exons that are covered or
        not covered across multiple samples.

        Args:
            sample_id (str): unique sample id
        """
        if exon_ids:
            query = self.query().filter(Exon.exon_id.in_(exon_ids))
        else:
            query = self.query()

        level = "completeness_{}".format(level)

        all_query = (query.add_columns(Transcript.transcript_id)
                          .distinct(Transcript.transcript_id)
                          .join(Exon.transcripts))
        all_count = all_query.count()

        logger.debug('find out which exons failed')
        yield_query = (query.add_columns(Exon.exon_id)
                            .join(ExonStatistic.sample, ExonStatistic.exon)
                            .filter(ExonStatistic.metric == level,
                                    ExonStatistic.value < threshold,
                                    Sample.sample_id == sample_id))
        exons = [row[0] for row in yield_query]
        transcripts = self.exon_transcripts(exons)

        tx_count = transcripts.count()
        diagnostic_yield = 100 - (tx_count/all_count * 100)
        return {
            "diagnostic_yield": diagnostic_yield,
            "count": tx_count,
            "total_count": all_count,
            "transcripts": transcripts
        }

    def completeness_levels(self):
        """Return a list of included completeness levels."""
        metrics = (self.query(ExonStatistic.metric)
                       .distinct(ExonStatistic.metric))
        # for all completeness levels, extract the level as int and full name
        levels = ((int(field[0].split('_')[-1]), field[0])
                  for field in metrics
                  if field[0].startswith('completeness'))
        # sort them based on the level int
        sorted_levels = sorted(levels, key=lambda level: list_get(level, 0))
        return sorted_levels
