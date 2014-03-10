__author__ = 'Kristo Koert'

import urllib2


class ICalRetriever:

    def __init__(self, url, file_path):
        """
            :param url url Where the information is downloaded from
            :type url str
            :param file_path Where the information is written
            :type file_path str
        """
        self.url = url
        self.file_path = file_path

    def retrieve(self):
        """Retrieves ical info from url and writes it to the specified text file."""
        response = urllib2.urlopen(
            self.url)
        write_to = file(self.file_path, "w")
        write_to.write(response.read())

if __name__ == "__main__":
    import subprocess
    ical_path = subprocess.check_output("pwd", shell=True)[:-1] + "/user_ical"
    tr = ICalRetriever(
        "https://itcollege.ois.ee/timetable/ical?student_id=3117&key=34c0482c0c579f1a7da0ea0ba6bda3077d356da8",
        ical_path)
    tr.retrieve()