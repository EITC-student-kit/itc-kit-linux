__author__ = 'Kristo Koert'

from datetime import datetime

class DataTypesAbstractClass():
    """Any classes inheriting from this class would be meant for creating instances that can be easily written to
    database, created from database rows or add the ability to safely and easily remove instances from database"""

    type_of = None

    def __init__(self, type_of):
        try:
            assert type_of in ("Class", "Mail", "Reminder", "Productive", "Neutral", "Counter-Productive")
            self.type_of = type_of
        except AssertionError:
            print("Parameter type_of should be Class, Mail, Reminder or Activity Type.")
            raise RuntimeError

    def get_database_row(self):
        raise NotImplementedError

    def remove_from_db(self):
        if self.type_of == "Class":
            pass
        elif self.type_of == "Mail":
            pass
        elif self.type_of == "Reminder":
            pass
        elif self.type_of in ("Productive", "Neutral", "Counter-Productive"):
            pass


#Raw prototype
class Mail(DataTypesAbstractClass):

    def __init__(self, title, sender):
        DataTypesAbstractClass.__init__(self, "Mail")
        self.title = title
        self.sender = sender

    def get_database_row(self):
        return self.title, self.sender, self.type_of


class Activity(DataTypesAbstractClass):

    def __init__(self, type_of, start, end, time_spent):
        DataTypesAbstractClass.__init__(self, type_of)
        self.time_spent = time_spent
        self.start = start
        self.end = end

    def get_database_row(self):
        return self.type_of, self.start, self.end, self.time_spent


class Notification(DataTypesAbstractClass):

    def __init__(self, message, timestamp, type_of):
        """
        :param message: A notification name
        :type message: str
        :param timestamp: The time this notification should be raised.
        :type timestamp: Timestamp
        :param type_of: Either aClass, Mail or Reminder
        :type type_of: str
        """
        DataTypesAbstractClass.__init__(self, type_of)
        self.message = message
        self.timestamp = timestamp

    def is_due(self):
        return self.timestamp <= datetime.now()

    def get_database_row(self):
        return self.type_of, self.timestamp, self.message


class Reminder(Notification):

    def __init__(self, message, time):
        """
            :param message: The message displayed on reminder activation.
            :type message: str
            :param time: Time when reminder should activate.
            :type time: Timestamp
        """
        Notification.__init__(self, message, time, "Reminder")


class AClass(Notification):
    """A data container for database writing and reading."""

    def __init__(self, subject_name, subject_code, attending_groups, class_type, start_timestamp, end_timestamp,
                 classroom, academician, attendible=False):
        """
        :param subject_code: The subjects code (e.g. I241).
        :type subject_code: str
        :param subject_name: The name of the class.
        :type subject_name: str
        :param attending_groups: Attending groups separated by comas.
        :type attending_groups: str
        :param class_type: Lecture, Exercise, Practice, Repeat prelim, Reservation, Consultation etc.
        :type class_type: str
        :param start_timestamp: Class starts at.
        :type start_timestamp: Timestamp
        :param end_timestamp: Class ends at.
        :type end_timestamp: Timestamp
        :param classroom: Where class takes place.
        :type classroom: str
        :param academician: The academician(s), format separated with comas.
        :type academician: str
        :param attendible: Does the user attend this class or not
        :type attendible: bool
        """
        Notification.__init__(self, subject_name, start_timestamp, "Class")
        self.subject_name = subject_name
        self.subject_code = subject_code
        self.attending_groups = attending_groups
        self.class_type = class_type
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.classroom = classroom
        self.academician = academician
        self.attendible = attendible

    def get_database_row(self):
        return (self.subject_code, self.subject_name, self.attending_groups, self.class_type, self.start_timestamp,
                self.end_timestamp, self.classroom, self.academician, self.attendible)

    def __str__(self):
        return str(self.get_database_row())
