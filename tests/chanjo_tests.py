from nose.tools import *
from chanjo.chanjo import Chanjo
from chanjo.bigBed import CoverageAdaptor
from chanjo.ccds import ElementAdaptor


class TestClass:
    def __init__(self):
        self.chanjo = Chanjo()

        self.coverage = CoverageAdaptor()
        self.elements = ElementAdaptor()

        #setattr(self, "{}s".format(element.lower()), self.dfs[element])

    def setUp(self):
        print "SETUP!"
        # Load in all the CCDS annotations
        self.chanjo.importAnnotations("tests/data/CCDS.current.txt")

    def tearDown(self):
        print "TEAR DOWN!"

    def test_open(self):
        assert_equal(self.test.path, "tests/data/CCDS.current.txt")
