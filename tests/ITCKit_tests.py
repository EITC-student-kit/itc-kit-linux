import unittest
from datetime import datetime

from ITCKit.utils import converting
from ITCKit.timetable import ical
from ITCKit.db import databaseConnector
from ITCKit.core import datatypes


class TestDatatypes(unittest.TestCase):

    def test_notification(self):
        dt = datetime.now()
        notif = datatypes.Notification("Some Type", "Remember to water plants", dt)
        self.assertEquals(notif.get_database_row(), ("Some Type", "Remember to water plants", dt))

    def test_reminder(self):
        dt = datetime.now()
        reminder = datatypes.Reminder("Remember to water plants", dt)
        self.assertEquals(reminder.get_database_row(), ("Reminder", "Remember to water plants", dt))

    def test_activity(self):
        dt1 = datetime.now()
        dt2 = datetime.now()
        activity = datatypes.Activity("Productive", dt1, dt2, 10)
        self.assertEquals(activity.get_database_row(), ("Productive", dt1, dt2, 10))

    def test_mail(self):
        mail = datatypes.Mail("ITC")
        self.assertEquals(mail.get_database_row()[:-1], ("Mail", "ITC"))

    def test_a_class(self):
        dt1 = datetime.now()
        dt2 = datetime.now()
        a_class = datatypes.AClass("I290", "Math", "12, 13, 14", "Practice", dt1, dt2,
                                   "213A", "Max", False)
        self.assertEquals(a_class.get_database_row(), ("I290", "Math", "12, 13, 14", "Practice", dt1,
                                                       dt2, "213A", "Max", False))


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