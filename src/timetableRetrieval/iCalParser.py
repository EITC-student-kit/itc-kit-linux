# -*- coding: utf-8 -*-
__author__ = 'Kristo Koert'
from src.utilityFunctions import UtilityFunctions
from src.utilityFunctions.UtilityFunctions import string_till_symbol, ical_datetime_to_timestamp
from src.dataTypes.aClass import AClass


class ICalParser():

    _subject_codes = []
    _subject_names = []
    _attending_groups = []
    _class_types = []
    _start_timestamps = []
    _end_timestamps = []
    _classrooms = []
    _academicians = []
    _user_attends = []
    classes = []

    def __init__(self):
        self.user_ical_file = file(UtilityFunctions.own_path() + "/timetableRetrieval/user_ical", "r")
        self.main_ical_file = file(UtilityFunctions.own_path() + "/timetableRetrieval/main_ical", "r")

    def _extract_vevents(self):
        """:return A list of vevents in string format"""
        found_start = False
        found_end = False
        vevent = ""
        vevents = []

        for line in self.user_ical_file:
            if "BEGIN:VEVENT" in line:
                found_start = True
            if "END:VEVENT" in line:
                found_end = True
            if found_start:
                vevent += line
            if found_start and found_end:
                vevents.append(vevent)
                found_start = False
                found_end = False
                vevent = ""
        return vevents

    def _get_parameters(self):
        """Collects all the AClass object creation parameters and stores them."""
        vevents = self._extract_vevents()

        for vevent in vevents:
            self._start_timestamps.append(ical_datetime_to_timestamp(string_till_symbol(vevent[vevent.find("DTSTART"):],
                                                                                  "00Z")[8:]))
            self._end_timestamps.append(ical_datetime_to_timestamp(string_till_symbol(vevent[vevent.find("DTEND"):],
                                                                                "00Z")[6:]))
            self._subject_names.append(string_till_symbol(vevent[vevent.find("SUMMARY"):], "[")[8:])
            description_line = string_till_symbol(vevent[vevent.find("DESCRIPTION:"):], "LOCATION")
            self._parse_description_line(description_line)

    def _parse_description_line(self, description_line):
        """
            :type description_line: str
            :return list
        """
        aclass_parameters = []
        keywords = ["Ainekood: ", "Rühmad: ", "Tüüp: ", "Ruum: ", "Õppejõud: "]
        for word in keywords:
            keyword_start_index = description_line.find(word)
            aclass_parameters.append(string_till_symbol(description_line[keyword_start_index + len(word): -1],
                                                        "\\n").replace("\\", ""))
        self._subject_codes.append(aclass_parameters[0])
        self._attending_groups.append(aclass_parameters[1])
        self._class_types.append(aclass_parameters[2])
        self._classrooms.append(aclass_parameters[3])
        self._academicians.append(aclass_parameters[4])

    def _create_class_instances(self):
        for i in range(len(self._subject_codes)):
            self.classes.append(AClass(self._subject_codes[i], self._subject_names[i], self._attending_groups[i],
                                       self._class_types[i], self._start_timestamps[i], self._end_timestamps[i],
                                       self._classrooms[i], self._academicians[i], False))

    def get_classes(self):
        self._get_parameters()
        self._create_class_instances()
        return self.classes

if __name__ == "__main__":
    icp = ICalParser()
    print icp.get_classes()

__author__ = 'Kristo Koert'

from timetableRetrieval.iCalParser import ICalParser
from database.databaseConnector import DatabaseConnector

if __name__ == "__main__":
    icp = ICalParser()
    dbc = DatabaseConnector()
    for aClass in icp.get_classes():
        dbc.add_class(aClass)
    print dbc.test()