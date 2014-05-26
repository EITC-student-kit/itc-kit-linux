try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='itc-kit',
      description='A toolkit for Estonian IT college students.',
      author='Kristo Koert, Johannes Vatsfeld',
      author_email='kristo.koert@itcollege.ee',
      url='https=//github.com/EITC-student-kit/itc-kit-linux',
      packages=['itc_kit', 'itc_kit.core', 'itc_kit.db', 'itc_kit.gui', 'itc_kit.mail', 'itc_kit.settings',
                'itc_kit.timetable', 'itc_kit.utils', 'itc_kit.gui.icons', "itc_kit.conky"],
      version='0.9')
