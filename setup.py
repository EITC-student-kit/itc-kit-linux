try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A toolkit for Estonian IT college students.',
    'author': 'Kristo Koert',
    'url': 'https://github.com/KristoKoert/ITCKit',
    'download_url': 'https://github.com/KristoKoert/ITCKit/archive/master.zip',
    'author_email': 'Kristo Koert',
    'version': '0.1',
    'install_requires': ['Python3.3', 'sqlLite', 'GTK++3', 'gobject-introspection'],
    'packages': ['ITCKit'],
    'scripts': [],
    'name': 'ITCKit'
}

setup(**config)