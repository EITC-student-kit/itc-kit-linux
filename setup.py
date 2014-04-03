try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A toolkit for Estonian IT college students.',
    'author': 'Kristo Koert',
    'url': 'https://github.com/KristoKoert/ITCKit',
    'download_url': 'https://github.com/KristoKoert/ITCKit/archive/master.zip',
    'author_email': 'kristo.koert@itcollege.ee',
    'version': '0.1',
    'install_requires': [], #'gobject-introspection' 'GTK+3' 'python3', 'python3-gi', 'python3-keyring'
    'packages': ['ITCKit'],
    'scripts': [],
    'name': 'ITCKit'
}

setup(**config)