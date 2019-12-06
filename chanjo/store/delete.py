import json
import logging

from sqlalchemy.sql import func

from chanjo.store.models import Sample, Transcript, TranscriptStat

LOG = logging.getLogger(__name__)

class DeleteMixin:

    """Methods for deleting samples from database"""

    def delete_sample(self, sample_id):
        """Delete single sample from database"""
        sample = [result for result in self.sample(sample_id=sample_id)]
        if len(sample) > 0:
            LOG.info("Deleting sample %s from database", sample[0].id)
            self.delete_commit(sample)
        else:
            LOG.info("No sample with name %s", sample_id)


    def delete_group(self, group_id):
        """Delete entire group from database"""
        LOG.info("Deleting entire group %s from database", group_id)
        samples = self.sample(group_id=group_id)
        for sample in samples:
            LOG.info("Deleting sample %s from database", sample.id)
            self.delete_commit(sample)
