__author__ = 'Kristo Koert'

from sqlite3 import connect, OperationalError, PARSE_DECLTYPES
import os
from ITCKit.core.datatypes import Notification, AClass, Activity, Reminder
from datetime import datetime

DATABASE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/itckitdb"

dt = datetime.now()
notif_cls = Notification('', dt, '').__class__
activ_cls = Activity('Productive', dt, dt, 1).__class__
a_cls_cls = AClass('', '', '', '', dt, dt, '', '', False).__class__
remin_cls = Reminder('', dt).__class__

table_dict = {notif_cls: ("Notification", "(?,?,?)"),
              activ_cls: ("Activity", "(?,?,?,?)"),
              a_cls_cls: ("Class", "(?,?,?,?,?,?,?,?,?)"),
              remin_cls: ("Notification", "(?,?,?)")}


def add_to_db(datatypes):
    """Adds instances from datatype to correct table. Duplicates are not written.
    :type datatypes Iterable | DataTypesAbstractClass
    """
    new = []
    try:
        iter(datatypes)
    except TypeError:
        datatypes = [datatypes]
    db = connect_to_db()
    cls = datatypes[0].__class__
    table_name = table_dict[cls][0]
    db_coloumns = table_dict[cls][1]
    new = get_not_already_in_db(datatypes, table_name)
    db.executemany(
        "INSERT INTO " + table_name + " VALUES "
        + db_coloumns, [cls.get_database_row() for cls in new])
    db.commit()


def get_not_already_in_db(datatypes, table_name):
    new = []
    if table_name == "Class":
        currently_in_db = get_all_classes()
        for datatype in datatypes:
            if datatype not in currently_in_db:
                new.append(datatype)
        return new
    else:
        return datatypes


def connect_to_db():
    """rtype: Connection"""
    db = connect(DATABASE_PATH, detect_types=PARSE_DECLTYPES)
    attempt_tables_creation(db.cursor())
    return db


def get_all_classes():
    """Not used outside testing. Returns database rows not instances of objects.
    :rtype tuple"""
    db = connect_to_db()
    db_rows = db.cursor().execute("SELECT * FROM Class").fetchall()
    classes = []
    for r in db_rows:
        classes.append(AClass(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
    return classes


def get_all_notifications():
    """:rtype tuple"""
    db = connect_to_db()
    ret_list = []
    params = db.cursor().execute("SELECT * FROM Notification").fetchall()
    for p in params:
        ret_list.append(Notification(p[0], p[1], p[2]))
    return ret_list


def get_all_activities():
    """Not used outside testing. Returns database rows not instances of objects.
    :rtype Iterable"""
    conn = connect_to_db()
    return conn.cursor().execute("SELECT * FROM Activity").fetchall()


def get_statistics():
    #ToDo implement statistics system
    pass


def remove_all_activities():
    db = connect_to_db()
    db.execute("DELETE * FROM Activity")
    db.commit()


def remove_all_notifications():
    db = connect_to_db()
    db.execute("DELETE * FROM Notification")
    db.commit()


def attempt_tables_creation(cursor):
    """If tables do not yet exist, they are created."""
    #ToDo implement a real check?
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
        cursor.execute("CREATE TABLE Notification (type TEXT, time TIMESTAMP, message TEXT)")
    except OperationalError:
        #Already exists
        pass

if __name__ == "__main__":
    pass