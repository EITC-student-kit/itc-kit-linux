__author__ = 'Kristo Koert'

import unittest

#Units
from iCalParser import ICalParser
from iCalRetriever import ICalRetriever


class ICalToolsTesting(unittest.TestCase):

    icr = ICalRetriever(False)
    icp = ICalParser()

    def test_retrieval(self):
        self.icr.retrieve()

    def test_parser(self):
        clss = self.icp.get_classes()
        for c in clss:
            print c


if __name__ == '__main__':
    unittest.main()
