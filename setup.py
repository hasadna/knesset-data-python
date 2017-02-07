#!/usr/bin/env python
from setuptools import setup, find_packages
import os, sys

if os.getenv("TRAVIS_TAG", "") != "" and os.getenv("TRAVIS_REPO_SLUG", "") == "hasadna/knesset-data-python":
    # this is a travis build eligible for publishing to pypi
    # get the version number from the tag name
    version = os.getenv("TRAVIS_TAG").lstrip("v")
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
