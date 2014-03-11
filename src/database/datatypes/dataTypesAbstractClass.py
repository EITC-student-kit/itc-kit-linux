__author__ = 'Kristo Koert'


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
