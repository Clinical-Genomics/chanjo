from pathlib import Path

import logging

LOG = logging.getLogger(__name__)

def fake_urlretrieve(url, target):
    open(target, 'a').close()


class FakeZipFile(object):

    def __init__(self, in_path, mode='r'):
        self.in_path = in_path

    def extractall(self, target_dir):
        LOG.info(f"fake zip target dir : {target_dir} path {self.in_path}")
        out_path = Path(target_dir).joinpath(self.in_path.name.replace('.zip', ''))
        open(out_path, 'a').close()
