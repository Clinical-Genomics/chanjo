"""Module for fetching from database"""

from chanjo.store.models import Sample, TranscriptStat


class FetchMixin:

    """Methods for fetching from database"""

    def fetch_samples(self, sample_id=None, group_id=None):
        """
            Fetch samples from database
        """
        query = self.query(Sample)
        if sample_id:
            query = query.filter(Sample.id == sample_id)
        if group_id:
            query = query.filter(Sample.group_id == group_id)
        return query

    def fetch_transcripts(self, sample_id):
        """
            Fetch transcripts from database
        """
        query = self.query(TranscriptStat).filter(
            TranscriptStat.sample_id == sample_id
        )
        return query
