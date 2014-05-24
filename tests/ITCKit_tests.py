import unittest
from datetime import datetime

from itc_kit.utils import converting, tools
from itc_kit.timetable import ical
from itc_kit.db import dbc
from itc_kit.core import datatypes
from itc_kit.core.datatypes import Activity, EMail, Reminder, AClass


class TestDatatypes(unittest.TestCase):

    def test_reminder(self):
        dt = datetime.now()
        reminder = datatypes.Reminder("Remember to water plants", dt)
        self.assertEquals(reminder.get_database_row(), ("Reminder", dt, "Remember to water plants", ))

    def test_activity(self):
        dt1 = datetime.now()
        dt2 = datetime.now()
        activity = datatypes.Activity("Productive", dt1, dt2, 10)
        self.assertEquals(activity.get_database_row(), ("Productive", dt1, dt2, 10))

    def test_mail(self):
        mail = datatypes.EMail("ITC")
        self.assertEquals(mail.get_database_row()[0:3:2], ("EMail", "ITC"))

    def test_a_class(self):
        dt1 = datetime.now()
        dt2 = datetime.now()
        a_class = datatypes.AClass("I290", "Math", "12, 13, 14", "Practice", dt1, dt2,
                                   "213A", "Max", False)
        self.assertEquals(a_class.get_database_row(), ("I290", "Math", "12, 13, 14", "Practice", dt1,
                                                       dt2, "213A", "Max", False))

    def test_est_timezone(self):
        est = datatypes.EstonianTimezone()
        time_x = datetime.now()
        cut_off = len(str(time_x))
        time_a = datetime(2014, 1, 20, 3, tzinfo=est) # Before daylight saving +02
        time_b = datetime(2014, 12, 20, 3, tzinfo=est) # After daylight saving +02
        time_c = datetime(2014, 5, 25, 3, tzinfo=est) # During daylight saving +03
        self.assertEqual(str(datetime(time_a, tzinfo=est))[0:cut_off], "+02:00")
        self.assertEqual(str(datetime(time_b, tzinfo=est))[0:cut_off], "+02:00")
        self.assertEqual(str(datetime(time_c, tzinfo=est))[0:cut_off], "+03:00")


class TestIcal(unittest.TestCase):

    def test_retriever(self):
        ical.retrieve_icals()

    def test_parser(self):
        ical.parse_icals()


class TestUtils(unittest.TestCase):

    def test_sec_to_time(self):
        self.assertEquals("00:00:59", converting.sec_to_time(59))
        self.assertEquals("00:02:39", converting.sec_to_time(159))
        self.assertEquals("01:00:50", converting.sec_to_time(3650))

    def test_to_timestamp(self):
        import sqlite3
        self.assertEquals(converting.ical_datetime_to_timestamp("DTSTART:20140304T083000Z"),
                          sqlite3.Timestamp(2014, 3, 4, 10, 30, 0))


class TestDB(unittest.TestCase):

    def test_add_to_db(self):
        from itc_kit.timetable import ical
        ical.parse_icals()
        dt = datetime.now()
        dbc.add_to_db(AClass('', '', '', '', dt, dt, '', '', False))
        dbc.add_to_db(Reminder("Reminder name", dt))
        dbc.add_to_db(Activity("Productive", dt, dt, 10))
        dbc.add_to_db(EMail("Sender"))

    def test_reading_classes(self):
        classes = dbc.get_all_classes()


if __name__ == '__main__':
    unittest.main()