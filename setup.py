try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import subprocess

ROOT_PATH = "/usr/local/lib/python3.4/dist-packages"

setup(name='EITC-kit',
      description='A toolkit for Estonian IT college students.',
      author='Kristo Koert, Johannes Vatsfeld',
      author_email='kristo.koert@itcollege.ee',
      url='https=//github.com/EITC-student-kit/Linux-version',
      packages=['ITCKit', 'ITCKit.core', 'ITCKit.db', 'ITCKit.gui', 'ITCKit.mail', 'ITCKit.settings',
                'ITCKit.timetable', 'ITCKit.utils', 'ITCKit.gui.icon', "ITCKit.conky"],
      version='0.1')


def set_main_executable():

    def find_file_path(file):
        search_in = ROOT_PATH
        for root, dirs, files in os.walk(search_in):
            if file in files:
                path = os.path.join(root, file)
                return path

    main_path = find_file_path("EITC-kit.py")

    if main_path is not None:

        print("Found main script in -> ", main_path)

        try:
            move_to_bin_cmd = "cp " + main_path + " /usr/bin/"
            p = subprocess.Popen(move_to_bin_cmd, shell=True, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
            output, errors = p.communicate()
            print("command: ", move_to_bin_cmd)
            print("Output ->", output, "Errors->", errors)
            assert errors == b''
            try:
                make_executable_cmd = "chmod +x /usr/bin/EITC-kit.py"
                p = subprocess.Popen(make_executable_cmd, shell=True, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
                output, errors = p.communicate()
                print("command: ", make_executable_cmd)
                print("Output ->", output, "Errors->", errors)
                assert errors == b''
                try:
                    ans = ''
                    alias = ''
                    while ans not in ['y', 'n']:
                        ans = input("Use the default terminal shorthand (itc)? (y/n) ")
                    if ans == 'y':
                        alias = 'itc'
                    else:
                        while check_if_alias_exists(alias):
                            while alias == '':
                                alias = input("Enter an alias: (c to cancel)")
                                if alias == 'c':
                                    assert False
                    if not check_if_alias_exists(alias):
                        print("apparently alias: ", alias, " does not exist, so creating.")
                        create_alias_cmd = 'echo "alias {}=\'EITC-kit.py\'" >> ~/.bashrc'.format(alias)
                        p = subprocess.Popen(create_alias_cmd, shell=True, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
                        output, errors = p.communicate()
                        print("command: ", create_alias_cmd)
                        print("Output ->", output, "Errors->", errors)
                        assert errors == b''
                    print("Program can now be run in the terminal by typing", alias, ", AFTER reopening terminal.")
                except AssertionError:
                    print("Unable to create alias for 'EITC-kit.py'. Program can be run with the command 'EITC-kit.py'"
                          " but not 'itc'")
            except AssertionError:
                print("Unable to make '/usr/bin/EITC-kit.py' executable.")
        except AssertionError:
            print("Unable to copy {} to /usr/bin/".format(main_path))

        #sudo bash -c "echo 'text' >> /etc/bashrc"
    else:
        print("Unable to find EITC-kit. Can still be run manually..")


def check_if_alias_exists(alias):
    if alias == '':
        return True
    elif alias == 'itc':
        cmd = 'unalias itc'
    else:
        cmd = "alias {0} 2>/dev/null >/dev/null && echo \"{0} is already set as an alias\"".format(alias)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, errors = p.communicate()
    print("command: ", cmd)
    print("Output ->", output, "Errors->", errors)
    if errors is not None:
        raise AssertionError
    if output != b'':
        print(output)
        return True
    return False

set_main_executable()