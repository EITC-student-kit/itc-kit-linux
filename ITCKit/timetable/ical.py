__author__ = 'Kristo Koert'

from ITCKit.utils import converting, tools
from ITCKit.core.datatypes import AClass
from ITCKit.settings import settings


class ICalRetriever():

    def __init__(self):
        import os
        self.user_file_path = os.path.dirname(os.path.abspath(__file__)) + "/user_ical"
        self.main_file_path = os.path.dirname(os.path.abspath(__file__)) + "/main_ical"
        #ToDo account for access denied due to lacking permission

    @staticmethod
    def change_user_url(url):
        settings.set_user_url(url)

    @staticmethod
    def change_main_url(url):
        settings.set_main_url(url)

    def retrieve(self, user=False, main=False):
        """Downloads the icals to their respective files.
        :type user bool
        :type main bool
        """
        if user:
            try:
                open(self.user_file_path, "w").write(
                    tools.download_ical(settings.get_user_url()))
            except ValueError:
                print("User url, not defined.")
        if main:
            open(self.main_file_path, "w").write(
                tools.download_ical(settings.get_main_url()))


class ICalParser():

    _keywords = ["Subject code: ", "Groups: ", "Type: ", "DTSTART:", "DTEND:", "SUMMARY:",
                 "LOCATION:", "Academician: "]

    _parameters = {key: [] for key in _keywords}

    classes = []

    def __init__(self):
        import os
        self.user_ical_file = open(os.path.dirname(os.path.abspath(__file__)) + "/user_ical", "r")
        self.main_ical_file = open(os.path.dirname(os.path.abspath(__file__)) + "/main_ical", "r")

    def _set_parameters(self):
        """Collects all the AClass object creation parameters and stores them."""
        vevents = self._extract_vevents()

        for event in vevents:
            event = event.split('\n')
            [event.append(element) for element in event[8].replace("DESCRIPTION:", '').split('\\n')]
            del event[8]
            self._find(event)

    def _extract_vevents(self):
        """Returns a list of ical vevent lines."""
        found_start = found_end = False
        vevent = ""
        vevents = []
        #SubOptimal
        #For main ical
        for line in self.main_ical_file:
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

    def _find(self, event):
        """Finds and sets all the parameters in a line, if there are any.
        :param event A vevent string from a ical file
        :type event str
        """
        var = None
        for data in event:
            for key in self._keywords:
                if key in data:
                    var = data[data.index(key):].replace(key, '')
                    if key == "DTSTART:" or key == "DTEND:":
                        self._parameters[key].append(converting.ical_datetime_to_timestamp(var))
                    else:
                        self._parameters[key].append(var.replace('\\', ''))
                #ToDo replace temporary fix
                elif key == "Academician: " and len(self._parameters["DTSTART:"]) > len(self._parameters["Academician: "]):
                    self._parameters[key].append('')

    def _create_class_instances(self):
        par = self._parameters
        for i in range(len(self._parameters["DTSTART:"])):
            #SUMMARY: returns name
            self.classes.append(AClass(par["SUMMARY:"][i], par["Subject code: "][i], par["Groups: "][i],
                                       par["Type: "][i], par["DTSTART:"][i], par["DTEND:"][i], par["LOCATION:"][i],
                                       par["Academician: "][i], False))

    def get_classes(self):
        """Gets all the parameters and creates instances.
        :rtype list
        """
        self._set_parameters()
        self._create_class_instances()
        return self.classes


if __name__ == "__main__":
    pass

