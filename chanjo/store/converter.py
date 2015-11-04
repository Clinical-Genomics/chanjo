# -*- coding: utf-8 -*-
from .models import Exon, ExonStatistic, Gene, Sample, Transcript


class ChanjoConverterMixin(object):

    """Mixin to provide conversions between genomic elements."""

    def gene_transcripts(self, *gene_ids):
        """Fetch transcripts related to a list of genes.

        Args:
            *gene_ids (List[str]): gene ids

        Returns:
            List[Transcript]: transcript objects related to the genes
        """
        query = (self.query(Transcript)
                     .distinct(Transcript.transcript_id)
                     .join(Exon.transcripts)
                     .filter(Gene.gene_id.in_(gene_ids)))
        return query

    def gene_exons(self, *gene_ids):
        """Fetch exons related to a list of genes.

        Args:
            *gene_ids (List[str]): gene ids

        Returns:
            List[Exon]: exon objects related to the genes
        """
        query = (self.query(Exon)
                     .distinct(Exon.exon_id)
                     .join(Exon.transcripts, Transcript.gene)
                     .filter(Gene.gene_id.in_(gene_ids)))
        return query

    def transcript_genes(self, transcript_ids, db_ids=False):
        """Fetch a lists of genes related to some exons.

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

    def transcript_exons(self, *transcript_ids):
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

    def exon_transcripts(self, exons_ids, db_ids=False):
        """Fetch a unique list of transcripts related to some exons.

        Args:
            exon_ids (List[str]): list of exon ids
            db_ids (Optional[bool]): if sending in primary key ids

        Returns:
            List[Transcript]: transcripts related to the exons
        """
        results = (self.query(Transcript)
                       .distinct(Transcript.transcript_id)
                       .join(Transcript.exons))
        if db_ids:
            results = results.filter(Exon.id.in_(exons_ids))
        else:
            results = results.filter(Exon.exon_id.in_(exons_ids))
        return results

    def exon_genes(self, *exon_ids):
        """Fetch unique genes related to a list of exons.

        Args:
            *exon_ids (List[str]): exon ids

        Returns:
            List[Gene]: gene objects related to the exons
        """
        query = (self.query(Gene)
                     .distinct(Gene.gene_id)
                     .join(Gene.transcripts, Transcript.exons)
                     .filter(Exon.exon_id.in_(exon_ids)))
        return query
