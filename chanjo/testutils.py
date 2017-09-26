import os


def fake_urlretrieve(url, target):
    open(target, 'a').close()


class FakeZipFile(object):

    def __init__(self, in_path, mode='r'):
        self.in_path = in_path

    def extractall(self, target_dir):
        out_path = os.path.join(target_dir, self.in_path.replace('.zip', ''))
        open(out_path, 'a').close()
