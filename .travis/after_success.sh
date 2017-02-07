#!/usr/bin/env bash

set -e  # exit on errors

[ -f .travis/.env ] && source .travis/.env

if [ "${TRAVIS_TAG}" != "" ] && [ "${TRAVIS_REPO_SLUG}" == "hasadna/knesset-data-python" ] && [ "${TRAVIS_PYPI_USER}" != "" ] && [ "${TRAVIS_PYPI_PASS}" != "" ]; then
    echo "publishing tagged release to pypi"
    echo "${TRAVIS_TAG}" > VERSION.txt
    echo "[distutils]
index-servers=pypi
[pypi]
repository = https://upload.pypi.org/legacy/
username = ${TRAVIS_PYPI_USER}
password = ${TRAVIS_PYPI_PASS}" > "${HOME}/.pypirc"
    ./setup.py bdist_wheel upload
else
    echo "skipping publishing to pypi because not a tagged release or not under hasadna repo"
fi
