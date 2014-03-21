__author__ = 'Kristo Koert'

from datetime import datetime


class DataTypesAbstractClass():
    """Any classes inheriting from this class would be meant for creating instances that can be easily written to
    database, created from database rows or add the ability to safely and easily remove instances from database"""

    _db_row = []

    def __init__(self):
        pass

    def _create_database_row(self, *kwargs):
        if len(self._db_row) == 0:
            self._db_row = kwargs

    def get_database_row(self):
        return self._db_row


class Notification(DataTypesAbstractClass):

    def __init__(self, type_of, message, when_to_raise):
        """
        :param type_of: Either Mail or Reminder
        :type type_of: str
        :type message: str
        :type when_to_raise: Timestamp
        """
        DataTypesAbstractClass.__init__(self)
        self._create_database_row(type_of, message, when_to_raise)

    def is_due(self):
        return self._db_row[2] <= datetime.now()


class Activity(DataTypesAbstractClass):

    def __init__(self, type_of, start, end, time_spent):
        """
        :param type_of: Either Productive, Neutral of Counter Productive
        :type type_of: str
        :type start: datetime
        :type end: datetime
        :type time_spent: int
        """
        DataTypesAbstractClass.__init__(self)
        self._create_database_row(type_of, start, end, time_spent)


class Mail(Notification):

    def __init__(self, sender):
        """
        :type sender: str
        """
        Notification.__init__(self, "Mail", sender, datetime.now())


class Reminder(Notification):

    def __init__(self, message, when_to_activate):
        """
            :type message: str
            :type when_to_activate: Timestamp
        """
        Notification.__init__(self, "Reminder", message, when_to_activate)


class AClass(DataTypesAbstractClass):
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
        DataTypesAbstractClass.__init__(self)
        self._create_database_row(subject_code, subject_name, attending_groups, class_type, start_timestamp,
                                  end_timestamp, classroom, academician, attendible)

    def __str__(self):
        return str(self.get_database_row())


if __name__ == "__main__":
    pass