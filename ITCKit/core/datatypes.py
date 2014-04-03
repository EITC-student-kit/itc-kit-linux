__author__ = 'Kristo Koert'

from datetime import datetime
from ITCKit.utils.converting import str_to_datetime


class DataTypesAbstractClass():
    """Any classes inheriting from this class would be meant for creating instances that can be easily written to
    database, created from database rows or add the ability to safely and easily remove instances from database"""

    def __init__(self):
        self._db_row = []

    def _create_database_row(self, *kwargs):
        """Sets the supplied parameters as the value for instances database row representation. Only works if a
        database row has not already been created, thus ensuring that inheritance can be used."""
        if len(self._db_row) == 0:
            self._db_row = kwargs

    def get_database_row(self):
        return self._db_row

    def __eq__(self, other):
        return self.get_database_row() == other.get_database_row()

    def __str__(self):
        return str(self.get_database_row())


class Notification(DataTypesAbstractClass):

    def __init__(self, type_of, when_to_raise, message):
        """The database table -> Notification (type TEXT, time TIMESTAMP, message TEXT)

        :param type_of: Either EMail or Reminder
        :type type_of: str
        :type message: str
        :type when_to_raise: Timestamp | str
        """
        try:
            if not isinstance(when_to_raise, datetime):
                when_to_raise = str_to_datetime(when_to_raise)
        except TypeError:
            print("Problem converting string to datetime in Notification class.")
            raise RuntimeError

        DataTypesAbstractClass.__init__(self)
        self._create_database_row(type_of, when_to_raise, message)

    def is_due(self):
        return self._db_row[1] <= datetime.now()


class Activity(DataTypesAbstractClass):

    def __init__(self, type_of, start, end, spent_time):
        """The database table -> Activity (activity_type TEXT, start_timestamp TIMESTAMP, end_timestamp TIMESTAMP,
         spent_time INTEGER )

        :param type_of: Either Productive, Neutral of Counterproductive
        :type type_of: str
        :type start: datetime
        :type end: datetime
        :type spent_time: int
        """
        try:
            assert type_of in ("Productive", "Neutral", "Counterproductive")
        except AssertionError:
            print("Invalid parameter passed for type_of in Activity instance creation: ", type_of)

        DataTypesAbstractClass.__init__(self)
        self._create_database_row(type_of, start, end, spent_time)


class EMail(Notification):

    def __init__(self, sender):
        """
        :type sender: str
        """
        Notification.__init__(self, "EMail", datetime.now(), sender)


class Reminder(Notification):

    def __init__(self, message, when_to_activate):
        """
        :type message: str
        :type when_to_activate: Timestamp
        """
        Notification.__init__(self, "Reminder", when_to_activate, message)


class AClass(DataTypesAbstractClass):

    def __init__(self, subject_code, subject_name, attending_groups, class_type, start_timestamp, end_timestamp,
                 classroom, academician, attendible=False):
        """The database table -> Class (subject_code TEXT, subject_name TEXT, attending_groups TEXT,
                                class_type TEXT, start_timestamp TIMESTAMP, end_timestamp TIMESTAMP, classroom TEXT,
                                academician TEXT, user_attend BOOLEAN)

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

    def __eq__(self, other):
        """Last element attendible row in database can differ and still be the same description."""
        return self.get_database_row()[:-1] == other.get_database_row()[:-1]

if __name__ == "__main__":
    pass