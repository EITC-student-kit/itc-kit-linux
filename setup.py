try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='EITC-kit',
      description='A toolkit for Estonian IT college students.',
      author='Kristo Koert, Johannes Vatsfeld',
      author_email='kristo.koert@itcollege.ee',
      url='https=//github.com/EITC-student-kit/Linux-version',
      packages=['ITCKit', 'ITCKit.core', 'ITCKit.db', 'ITCKit.gui', 'ITCKit.mail', 'ITCKit.settings',
                'ITCKit.timetable', 'ITCKit.utils', 'ITCKit.gui.icon', "ITCKit.conky"],
      version='0.1')