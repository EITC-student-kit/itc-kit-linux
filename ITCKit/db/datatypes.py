__author__ = 'Kristo Koert'

from datetime import datetime


class DataTypesAbstractClass():
    """Any classes inheriting from this class would be meant for creating instances that can be easily written to
    database, created from database rows or add the ability to safely and easily remove instances from database"""

    _type_of = None

    def __init__(self, type_of):
        try:
            assert type_of in ("Class", "Mail", "Reminder")
        except AssertionError:
            print("Parameter type_of should be Class, Mail, Reminder.")
            raise RuntimeError
        self._type_of = unicode(type_of)

    def remove_from_database(self):
        if self._type_of == "Class":
            pass
        if self._type_of == "Reminder":
            pass
        if self._type_of == "Mail":
            pass

    def get_database_info(self):
        raise NotImplementedError


class Notification(DataTypesAbstractClass):
    """A data container for database writing and reading."""

    def __init__(self, message, timestamp, type_of):
        """
        :param message: A notification name
        :type message: str
        :param timestamp: The time this notification should be raised.
        :type timestamp: Timestamp
        :param type_of: Either aClass, Mail or Reminder
        :type type_of: str
        """
        #Unicode for database compatibility.
        DataTypesAbstractClass.__init__(self, type_of)
        self.message = unicode(message)
        self.timestamp = unicode(timestamp)

    def is_due(self):
        return self.timestamp <= datetime.now()

    def get_notification_info(self):
        return self.message, self.timestamp, self._type_of


class Reminder(Notification):

    def __init__(self, message, time):
        """
            :param message: The message displayed on reminder activation.
            :type message: str
            :param time: Time when reminder should activate.
            :type time: Timestamp
        """
        Notification.__init__(self, message, time, "Reminder")

    def get_database_info(self):
        return self.get_notification_info()


class AClass(Notification):
    """A data container for database writing and reading."""

    def __init__(self, subject_code, subject_name, attending_groups, class_type, start_timestamp, end_timestamp,
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
        self.subject_code = unicode(subject_code)
        self.subject_name = unicode(subject_name)
        self.attending_groups = unicode(attending_groups)
        self.class_type = unicode(class_type)
        self.start_timestamp = unicode(start_timestamp)
        self.end_timestamp = unicode(end_timestamp)
        self.classroom = unicode(classroom)
        self.academician = unicode(academician)
        self.attendible = unicode(attendible)

    def get_database_info(self):
        return (self.subject_code, self.subject_name, self.attending_groups, self.class_type, self.start_timestamp,
                self.end_timestamp, self.classroom, self.academician, self.attendible)
