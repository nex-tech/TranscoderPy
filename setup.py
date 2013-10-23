#!/usr/bin/python

from distutils.core import setup
from transcoder.utils import __version__


setup(
    name='transcoder',
    version=__version__,
    description='Integration library for the Nex-Tech transcoder',
    long_description=open('README.md', 'r').read(),
    author='Austin Gabel',
    author_email='agabel@gmail.com',
    url='https://github.com/nex-tech/TranscoderPy',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    install_requires=[
        'requests>=1.0'
    ],
    packages=[
        'transcoder',
    ],
    zip_safe=False,
)

