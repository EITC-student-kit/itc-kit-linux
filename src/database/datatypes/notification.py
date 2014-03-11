__author__ = 'Kristo Koert'

from datetime import datetime

from dataTypesAbstractClass import DataTypesAbstractClass


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

if __name__ == "__main__":
    pass