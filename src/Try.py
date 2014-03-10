__author__ = 'Kristo Koert'

from timetableRetrieval.iCalParser import ICalParser
from database.databaseConnector import DatabaseConnector

if __name__ == "__main__":
    icp = ICalParser()
    dbc = DatabaseConnector()
    for aClass in icp.get_classes():
        dbc.add_class(aClass)
    print dbc.test()