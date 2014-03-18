__author__ = 'Kristo Koert'

from sqlite3 import connect, OperationalError

from ITCKit.core.datatypes import Notification, AClass, Activity
from ITCKit.settings import DATABASE_PATH


def connect_to_db():
    """rtype: Connection"""
    db = connect(DATABASE_PATH)
    attempt_tables_creation(db.cursor())
    return db


def add_to_db(data):
    """
    :type data: Notification | AClass | Activity | list
    """
    if isinstance(data, list):
        if isinstance(data[0], Notification):
            add_notifications(data)
        if isinstance(data[0], AClass):
            add_classes(data)
        if isinstance(data[0], Activity):
            add_activities(data)
    else:
        if isinstance(data, Notification):
            add_notifications(data)
        if isinstance(data, AClass):
            add_classes(data)
        if isinstance(data, Activity):
            add_activities(data)


def add_classes(classes):
    """Adds instances of AClass to AClass table.
    :type classes Iterable | AClass
    """
    try:
        iter(classes)
    except TypeError:
        classes = [classes]
    db = connect_to_db()
    db.executemany(
        "INSERT INTO Class VALUES (?,?,?,?,?,?,?,?,?)", [cls.get_database_row() for cls in classes])
    db.commit()


def get_all_classes():
    """:rtype tuple"""
    db = connect_to_db()
    return db.cursor().execute("SELECT * FROM Class").fetchall()


def add_notifications(notifications):
    """Adds instances of Notification to Notification table.
    :type notifications: Iterable | Notification
    """
    try:
        iter(notifications)
    except TypeError:
        notifications = [notifications]
    db = connect_to_db()
    db.executemany(
        "INSERT INTO Notification VALUES (?,?,?)",
        [notif.get_database_row() for notif in notifications])
    db.commit()


def get_all_notifications():
    """:rtype tuple"""
    db = connect_to_db()
    return db.cursor().execute("SELECT * FROM Notification").fetchall()


def add_activities(activities):
    """Add an activity instance to Activity table.
    :type activities: Iterable | Activity
    """
    try:
        iter(activities)
    except TypeError:
        activities = [activities]
    db = connect_to_db()
    db.executemany(
        "INSERT INTO Activity VALUES (?, ?, ?, ?)",
        [act.get_database_row() for act in activities])
    db.commit()


def get_all_activities():
    """:rtype Iterable"""
    conn = connect_to_db()
    return conn.cursor().execute("SELECT * FROM Activity").fetchall()


def update_statistics(self, reminder):
    pass


def get_statistics(self):
    pass


def update_settings(self):
    pass


def get_settings(self):
    pass


def attempt_tables_creation(cursor):
    """If tables do not yet exist, they are created."""
    try:
        cursor.execute("""CREATE TABLE Class (subject_code TEXT, subject_name TEXT, attending_groups TEXT,
                                class_type TEXT, start_timestamp TIMESTAMP, end_timestamp TIMESTAMP, classroom TEXT,
                                academician TEXT, user_attend BOOLEAN)""")
    except OperationalError:
        #Already exists
        pass
    try:
        cursor.execute("""CREATE TABLE Activity (activity_type TEXT, start_timestamp TIMESTAMP,
                                end_timestamp TIMESTAMP, spent_time INTEGER )""")
    except OperationalError:
        #Already exists
        pass
    try:
        cursor.execute("""CREATE TABLE Settings (timemanager_enabled BOOLEAN, mail_enabled BOOLEAN,
                                conky_enabled BOOLEAN, user_name TEXT, password TEXT, conky_color TEXT,
                                timetable_update_interval INTEGER, conky_type INTEGER, user_timetable_url TEXT)""")
    except OperationalError:
        #Already exists
        pass
    try:
        cursor.execute("CREATE TABLE Notification (type TEXT, time TIMESTAMP, message TEXT)")
    except OperationalError:
        #Already exists
        pass

if __name__ == "__main__":
    pass