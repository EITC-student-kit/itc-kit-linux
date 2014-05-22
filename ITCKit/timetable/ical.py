__author__ = 'Kristo Koert'

from ITCKit.utils import converting, tools
from ITCKit.core.datatypes import AClass
from ITCKit.settings.settings import get_timetable_settings
from ITCKit.db import dbc

keywords = ["Subject code: ", "Groups: ", "Type: ", "DTSTART:", "DTEND:", "SUMMARY:",
            "LOCATION:", "Academician: "]


def _contains_keyword(line):
    for key in keywords:
        if key in line:
            return True
    return False


def _all_parameters_equal(parameters):
    """Checks if all the parameters are of equal length.
    :type parameters: dict
    :raises AssertionError"""
    number_of_events = len(parameters["DTSTART:"])
    for key in keywords:
        try:
            assert number_of_events == len(parameters[key])
        except AssertionError:
            print("Parameters are not of equal length.")
            [print(params, "->", len(parameters[params])) for params in parameters]


def _get_relevant_lines(ical_text):
    """Returns only the lines relevant for the processes in this file.
    :type ical_text: str
    :rtype: str"""
    relevant_text = ""
    ical_text = ical_text[ical_text.find("BEGIN:VEVENT"):]
    for line in ical_text.split('\n'):
        if "DESCRIPTION:" in line:
            line = line.replace("DESCRIPTION:", '')
            description_lines = line.split('\\n')
            for l in description_lines:
                if _contains_keyword(l):
                    relevant_text += l
                    relevant_text += '\n'
        elif _contains_keyword(line):
            relevant_text += line
    return relevant_text


def _write_to_user_ical(ical_text):
    user_file_path = get_timetable_settings()['user_ical_path']
    open(user_file_path, "w").write(_get_relevant_lines(ical_text))


def _write_to_main_ical(ical_text):
    main_file_path = get_timetable_settings()['user_ical_path']
    open(main_file_path, "w").write(_get_relevant_lines(ical_text))


def _format_parameters(old_parameters):
    """Parameters are converted to their proper forms.
    :type old_parameters: dict
    :rtype: dict"""
    new_parameters = {key: [] for key in keywords}
    for el in old_parameters["Groups: "]:
        new_parameters["Groups: "].append(el.replace('\\', ''))
    for el in old_parameters["SUMMARY:"]:
        new_parameters["SUMMARY:"].append(el[:el.find('[')])
    for el in old_parameters["DTEND:"]:
        new_parameters["DTEND:"].append(converting.ical_datetime_to_timestamp(el))
    for el in old_parameters["DTSTART:"]:
        new_parameters["DTSTART:"].append(converting.ical_datetime_to_timestamp(el))
    for key in keywords:
        if len(new_parameters[key]) == 0:
            new_parameters[key] = old_parameters[key]
    return new_parameters


def _collect_parameters(formatted_ical_text, parameters):
    """Recursively collects all the parameters
    :type formatted_ical_text: str
    :type parameters dict
    :rtype: dict
    """
    try:
        cut_off = formatted_ical_text.index("DTSTART:", 1)
        event = formatted_ical_text[0:cut_off]
        rest = formatted_ical_text[cut_off:]
        #Deals with events that do not have a Academician
        if len(event.split('\n')) == 8:
            event += "Academician: "
        for line in event.split('\n'):
            for key in parameters.keys():
                if key in line:
                    parameters[key].append(line.replace(key, ''))
        return _collect_parameters(rest, parameters)
    except ValueError:
        parameters = _format_parameters(parameters)
        _all_parameters_equal(parameters)
        return parameters


def _combine_classes(user_classes, main_classes):
    """Returns a list of only the AClass objects that are unique.
    :type user_classes: list
    :type main_classes: list
    :rtype: list
    """
    for cls in user_classes:
        if cls in main_classes:
            main_classes[main_classes.index(cls)] = cls
    return main_classes


def retrieve_icals():
    """Writes formatted icals to files. Raises value error if url invalid.
    :raises ValueError"""
    _settings = get_timetable_settings()

    try:
        main_ical = tools.download_ical(_settings["main_url"])
        _write_to_main_ical(main_ical)
    except ValueError:
        raise Exception("Main URL faulty, problem in programming.")

    if _settings["user_url"] != "":
        try:
            user_ical = tools.download_ical(_settings["user_url"])
            _write_to_user_ical(user_ical)
        except ValueError:
            raise Exception("Invalid URL! Please check URL.")


def parse_icals():
    """Parses ical files and writes the results to database."""
    parameters_dict = {key: [] for key in keywords}
    user_classes = []
    main_classes = []

    user_ical = open(get_timetable_settings()['main_ical_path'], "r").read()
    main_ical = open(get_timetable_settings()['user_ical_path'], "r").read()

    parameters = _collect_parameters(user_ical, parameters_dict)
    for i in range(len(parameters["DTSTART:"])):
        user_classes.append(AClass(parameters["Subject code: "][i], parameters["SUMMARY:"][i], parameters["Groups: "][i],
                                   parameters["Type: "][i], parameters["DTSTART:"][i], parameters["DTEND:"][i],
                                   parameters["LOCATION:"][i], parameters["Academician: "][i], True))

    parameters.clear()

    parameters = _collect_parameters(main_ical, parameters_dict)
    for i in range(len(parameters["DTSTART:"])):
        main_classes.append(AClass(parameters["Subject code: "][i], parameters["SUMMARY:"][i], parameters["Groups: "][i],
                                   parameters["Type: "][i], parameters["DTSTART:"][i], parameters["DTEND:"][i],
                                   parameters["LOCATION:"][i], parameters["Academician: "][i], False))

    dbc.add_to_db(_combine_classes(user_classes, main_classes))


def update_icals():
    try:
        retrieve_icals()
    except Exception as error_message:
        raise error_message
    parse_icals()