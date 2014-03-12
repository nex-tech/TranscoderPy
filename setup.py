#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Integration library for the Nex-Tech transcoder',
    'author': 'Austin Gabel',
    'author_email': 'agabel@gmail.com',
    'download_url': 'https://github.com/nex-tech/TranscoderPy',
    'version': '0.2',
    'classifiers': [
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    'install_requires': ['requests'],
    'packages': ['transcoder'],
    'zip_safe': False,
    'name': 'transcoder',
}

setup(**config)

