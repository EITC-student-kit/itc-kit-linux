import unittest

from ITCKit.utils import converting
from ITCKit.timetable import ical
from ITCKit.db import databaseConnector


class TestIcal(unittest.TestCase):

    icr = ical.ICalRetriever()
    icp = ical.ICalParser()

    def test_retriever(self):
        self.icr.retrieve(True, True)

    def test_parser(self):
        self.icp.get_classes()


class TestUtils(unittest.TestCase):

    def test_sec_to_time(self):
        self.assertEquals("00:00:59", converting.sec_to_time(59))
        self.assertEquals("00:02:39", converting.sec_to_time(159))
        self.assertEquals("01:00:50", converting.sec_to_time(3650))

    def test_to_timestamp(self):
        import sqlite3
        self.assertEquals(converting.ical_datetime_to_timestamp("DTSTART:20140304T080000Z"),
                          sqlite3.Timestamp(2014, 3, 4, 10, 0, 0))


class TestDatabaseConnector(unittest.TestCase):

    dbc = databaseConnector.DatabaseConnector()

    def test_writing_classes(self):
        icp = ical.ICalParser()
        classes = icp.get_classes()
        self.dbc.add_classes(classes)

    def test_reading_classes(self):
        classes = self.dbc.get_classes()
        for a_class in classes:
            self.assertNotIn('', a_class)

if __name__ == '__main__':
    unittest.main()

