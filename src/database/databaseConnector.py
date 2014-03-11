__author__ = 'Kristo Koert'

from sqlite3 import *


class DatabaseConnector():

    def __init__(self):
        self.conn = connect("itckitdata.db")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("""CREATE TABLE Class (subject_code TEXT, subject_name TEXT, attending_groups TEXT,
                                class_type TEXT, start_timestamp TIMESTAMP, end_timestamp TIMESTAMP, classroom TEXT,
                                academician TEXT, user_attend BOOLEAN)""")
        except OperationalError:
            print "Table Class already exists."
        try:
            self.cursor.execute("""CREATE TABLE TimemanagerActivity (activity_type TEXT, start_timestamp TIMESTAMP,
                                end_timestamp TIMESTAMP, spent_time INTEGER )""")
        except OperationalError:
            print "Table TimemanagerActivity already exists."
        try:
            self.cursor.execute("""CREATE TABLE Settings (timemanager_enabled BOOLEAN, mail_enabled BOOLEAN,
                                conky_enabled BOOLEAN, user_name TEXT, password TEXT, conky_color TEXT,
                                class_notifications BOOLEAN, timetable_update_interval INTEGER, conky_type INTEGER,
                                academician TEXT, user_timetable_url TEXT)""")
        except OperationalError:
            print "Table Settings already exists."
        try:
            self.cursor.execute("CREATE TABLE Notification (type TEXT, time TIMESTAMP, message TEXT)")
        except OperationalError:
            print "Table Notification already exists."

    def add_class(self, a_class):
        """
            :param a_class: A class
            :type a_class: aClass
        """
        self.cursor.execute("INSERT INTO Class VALUES (?,?,?,?,?,?,?,?,?)", (a_class.get_database_info()))

    def add_classes(self, classes):
        for cls in classes:
            self.add_class(cls)
        self.conn.commit()

    def add_notification(self, reminder):
        """
            :param reminder: A reminder
            :type reminder: Reminder
        """
        self.cursor.execute("INSERT INTO Notification VALUES (?,?,?)", (reminder.get_notification_type(),
                                                                        reminder.get_notification_timestamp(),
                                                                        reminder.get_notification_message()))
        self.conn.commit()

    def update_statistics(self, reminder):
        pass

    def get_classes(self):
        self.cursor.execute("SELECT * FROM Class")
        for row in self.cursor:
            print row

    def get_notifications(self):
        self.cursor.execute("SELECT * FROM Notification")

    def get_statistics(self):
        pass

if __name__ == "__main__":
    dbc = DatabaseConnector()
    dbc.get_classes()


