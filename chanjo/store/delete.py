"""Module for deleting from database"""

import logging
from chanjo.store.models import Sample

LOG = logging.getLogger(__name__)


class DeleteMixin:

    """Methods for deleting samples from database"""

    def delete_sample(self, sample_id):
        """Delete single sample from database"""
        samples = list(self.fetch_samples(sample_id=sample_id))
        if len(samples) > 0:
            with self.begin() as session:
                LOG.info("Deleting sample %s from database", samples[0].id)
                for sample in samples:
                    session.execute(sample.delete())

    def delete_group(self, group_id):
        """Delete entire group from database"""
        LOG.info("Deleting entire group %s from database", group_id)
        samples = self.fetch_samples(group_id=group_id)
        with self.begin() as session:
            for sample in samples:
                LOG.info("Deleting sample %s from database", sample.id)
                session.execute(sample.delete())
