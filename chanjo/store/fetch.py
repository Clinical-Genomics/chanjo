import json

from sqlalchemy.sql import func

from chanjo.store.models import Sample, Transcript, TranscriptStat

class FetchMixin:

    """Methods for fetching from database"""

    def sample(self, sample_id=None, group_id=None):
        query = self.query(Sample)
        if sample_id:
            query = query.filter(Sample.id.is_(sample_id))
        if group_id:
            query = query.filter(Sample.group_id.is_(group_id))
        return query

    def transcripts(self, sample_id):
        query = (self.query(TranscriptStat)
                     .filter(TranscriptStat.sample_id.is_(sample_id))
                     )
        return query
