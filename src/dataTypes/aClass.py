__author__ = 'Kristo Koert'

from notification import Notification


class AClass(Notification):

    def __init__(self, subject_code, subject_name, attending_groups, class_type, start_timestamp, end_timestamp,
                 classroom, academician, attendible=False):
        """Creates a representation of a single class.
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
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.attending_groups = attending_groups
        self.class_type = class_type
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.classroom = classroom
        self.academician = academician
        self.attendible = attendible
