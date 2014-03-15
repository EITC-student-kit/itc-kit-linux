__author__ = 'Kristo Koert'

from sqlite3 import connect, OperationalError

from ITCKit.settings import DATABASE_NAME


class DatabaseConnector():

    def __init__(self):
        """If tables do not yet exist, they are created."""
        self.conn = connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute("""CREATE TABLE Class (subject_code TEXT, subject_name TEXT, attending_groups TEXT,
                                class_type TEXT, start_timestamp TIMESTAMP, end_timestamp TIMESTAMP, classroom TEXT,
                                academician TEXT, user_attend BOOLEAN)""")
        except OperationalError:
            pass

        try:
            self.cursor.execute("""CREATE TABLE TimemanagerActivity (activity_type TEXT, start_timestamp TIMESTAMP,
                                end_timestamp TIMESTAMP, spent_time INTEGER )""")
        except OperationalError:
            pass

        try:
            self.cursor.execute("""CREATE TABLE Settings (timemanager_enabled BOOLEAN, mail_enabled BOOLEAN,
                                conky_enabled BOOLEAN, user_name TEXT, password TEXT, conky_color TEXT,
                                class_notifications BOOLEAN, timetable_update_interval INTEGER, conky_type INTEGER,
                                academician TEXT, user_timetable_url TEXT)""")
        except OperationalError:
            pass

        try:
            self.cursor.execute("CREATE TABLE Notification (type TEXT, time TIMESTAMP, message TEXT)")
        except OperationalError:
            pass

    def _add_class(self, a_class):
        """
            :param a_class: A class
            :type a_class: aClass
        """
        self.cursor.execute("INSERT INTO Class VALUES (?,?,?,?,?,?,?,?,?)", (a_class.get_database_row()))

    def add_classes(self, classes):
        for cls in classes:
            self._add_class(cls)
        self.conn.commit()

    def add_notification(self, notification):
        """
            :param notification: A reminder
            :type notification: Notification
        """
        self.cursor.execute("INSERT INTO Notification VALUES (?,?,?)", (notification.get_database_row()))
        self.conn.commit()

    def update_statistics(self, reminder):
        pass

    def get_classes(self):
        return self.cursor.execute("SELECT * FROM Class")

    def get_notifications(self):
        self.cursor.execute("SELECT * FROM Notification")

    def get_statistics(self):
        pass

if __name__ == "__main__":
    dbc = DatabaseConnector()
    dbc.get_classes()


