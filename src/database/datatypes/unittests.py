__author__ = 'Kristo Koert'

import unittest

#Units
from src.database.datatypes.aClass import AClass
from src.database.datatypes.reminder import Reminder
from sqlite3 import Timestamp


class DataTypesTesting(unittest.TestCase):

    reminder = Reminder("Message", Timestamp.now())
    a_class = AClass("code", "name", "groups", "practice", Timestamp.now(), Timestamp.now(), "cls room",
                         "academician", True)

    def test_unicode(self):
        for value in self.a_class.get_database_info():
            self.assertIs(type(value), unicode)

        for value in self.reminder.get_database_info():
            self.assertIs(type(value), unicode)

if __name__ == '__main__':
    unittest.main()
