__author__ = 'Kristo Koert'

from sqlite3 import connect, OperationalError
import os

from ITCKit.core.datatypes import Notification, AClass, Activity


DATABASE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/itckitdb"

from datetime import datetime

dt = datetime.now()
notif_cls = Notification('', '', dt).__class__
activ_cls = Activity('', dt, dt, 1).__class__
a_cls_cls = AClass('', '', '', '', dt, dt, '', '', False).__class__

table_dict = {notif_cls: ("Notification", "(?,?,?)"),
              activ_cls: ("Activity", "(?,?,?,?)"),
              a_cls_cls: ("Class", "(?,?,?,?,?,?,?,?,?)")}


def add_to_db(data_type):
    """Adds instances from datatype to correct table_name.
    :type data_type Iterable | AClass | Activity | Notification
    """
    try:
        iter(data_type)
    except TypeError:
        data_type = [data_type]
    db = connect_to_db()
    cls = data_type[0].__class__
    table_name = table_dict[cls][0]
    db_coloums = table_dict[cls][1]
    db.executemany(
        "INSERT INTO " + table_name + " VALUES "
        + db_coloums, [cls.get_database_row() for cls in data_type])
    db.commit()


def connect_to_db():
    """rtype: Connection"""
    db = connect(DATABASE_PATH)
    attempt_tables_creation(db.cursor())
    return db


def get_all_classes():
    """:rtype tuple"""
    db = connect_to_db()
    return db.cursor().execute("SELECT * FROM Class").fetchall()


def get_all_notifications():
    """:rtype tuple"""
    db = connect_to_db()
    return [[].append(Notification(p[0], p[1], p[2])
                      for p in db.cursor().execute("SELECT * FROM Notification").fetchall())]


def get_all_activities():
    """:rtype Iterable"""
    conn = connect_to_db()
    return conn.cursor().execute("SELECT * FROM Activity").fetchall()


def get_statistics(self):
    pass


def attempt_tables_creation(cursor):
    """If tables do not yet exist, they are created."""
    #ToDo implement a check
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
    add_to_db(Notification("Reminder", "Message", datetime.now()))
    print(get_all_notifications())
