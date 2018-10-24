# -*- coding: utf-8 -*-
from pprint import pprint as pp

from sqlalchemy.sql import func

from chanjo.store.models import Sample, Transcript, TranscriptStat

# COMPLETENESS_COLUMNS = ["completeness_{}".format(level) for level
#                         in COMPLETENESS_LEVELS]


class CalculateMixin:

    """Methods for calculating various metrics."""

    def mean(self, sample_ids=None, gene_ids=None):
        """Calculate the mean values of all metrics per sample."""
        pipeline = []
        query = {}
        if sample_ids:
            query = {
                '$match': {
                    'sample_id': {
                        '$in': ['sample1']
                    }
                }
            }
        if gene_ids:
            gene_ids = list(gene_ids)
            key = 'gene_id'
            try:
                int(gene_ids[0])
            except ValueError:
                key = 'gene_name'

            if not '$match' in query:
                query['$match'] = {}
            
            query['$match'][key] = {'$in': gene_ids}

            pipeline.append(query)

        group = {
            '$group': {
                '_id': '$sample_id',
                'mean_coverage': {
                    '$avg': '$mean_coverage'
                }, 
                'completeness_10': {
                    '$avg': '$completeness_10'
                }, 
                'completeness_15': {
                    '$avg': '$completeness_15'
                }, 
                'completeness_20': {
                    '$avg': '$completeness_20'
                }, 
                'completeness_50': {
                    '$avg': '$completeness_20'
                }, 
                'completeness_100': {
                    '$avg': '$completeness_20'
                }, 
            }
        }
        
        pipeline.append(group)

        res = self.transcript_stat_collection.aggregate(pipeline)
        
        return res

    def gene_metrics(self, *genes):
        """Calculate gene statistics."""
        query = self.mean(gene_ids=genes))
        
        return query
