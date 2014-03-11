__author__ = 'Kristo Koert'

import urllib2


class ICalRetriever:

    def __init__(self, user=True):
        import os
        if user:
            self.url = "https://itcollege.ois.ee/en/timetable/ical?student_id=3117&key=34c0482c0c579f1a7da0ea0ba6bda3077d356da8"
            self.file_path = os.path.dirname(os.path.abspath(__file__)) + "/user_ical"
        else:
            self.url = "https://itcollege.ois.ee/et/timetable/ical?curriculum_id=2&key=01d8d5cbdbb9881fbf103f61c36955e731531a28"
            self.file_path = os.path.dirname(os.path.abspath(__file__)) + "/main_ical"

    def retrieve(self):
        """Retrieves ical info from url and writes it to the specified text file."""
        response = urllib2.urlopen(
            self.url)
        write_to = file(self.file_path, "w")
        write_to.write(response.read())

if __name__ == "__main__":
    pass