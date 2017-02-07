#!/usr/bin/env python
from setuptools import setup, find_packages
import os, sys

if os.path.exists("VERSION.txt"):
    # this file can be written by CI tools (e.g. Travis)
    with open("VERSION.txt") as version_file:
        version = version_file.read().strip().strip("v")
else:
    version = "0.0.0"

setup(
    name='knesset-data',
    version=version,
    description='API for access to available Israeli Parliament (Knesset) data',
    author='Ori Hoch',
    author_email='ori@uumpa.com',
    license='GPLv3',
    url='https://github.com/hasadna/knesset-data-python',
    packages=find_packages(exclude=["tests", "test.*"]),
    install_requires=['beautifulsoup4', 'pyslet', 'requests', 'simplejson', 'pyth',
                      'python-hebrew-numbers', 'cached-property', 'octohub'],
)
