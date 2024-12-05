"""Module for deleting from database"""

import logging

from chanjo.store.models import Sample

LOG = logging.getLogger(__name__)


class DeleteMixin:
    """Methods for deleting samples from database"""

    def delete_sample(self, sample_id):
        """Delete single sample from database"""
        LOG.info(f"Deleting sample {sample_id} from database")
        with self.begin() as session:
            sample = session.get(Sample, sample_id)
            if sample:
                session.delete(sample)

    def delete_group(self, group_id):
        """Delete entire group from database"""
        LOG.info("Deleting entire group %s from database", group_id)
        samples = self.fetch_samples(group_id=group_id)
        with self.begin() as session:
            for sample in samples:
                LOG.info("Deleting sample %s from database", sample.id)
                session.execute(sample.delete())
