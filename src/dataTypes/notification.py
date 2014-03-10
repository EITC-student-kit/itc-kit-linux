__author__ = 'Kristo Koert'

from datetime import datetime


class Notification():
    """A notification abstraction"""

    def __init__(self, message, timestamp, type_of):
        """The created instance has a name and a timestamp for when it should be raised.

        :param message: A notification name
        :type message: str
        :param timestamp: The time this notification should be raised.
        :type timestamp: Timestamp
        """
        self._message = message
        self._timestamp = timestamp
        self._type = type_of

    def get_notification_message(self):
        return self._message

    def get_notification_timestamp(self):
        return self._timestamp

    def get_notification_type(self):
        return self._type

    def get_message(self):
        return self._message

    def is_due(self):
        return self._timestamp <= datetime.now()

if __name__ == "__main__":
    pass