#!/usr/bin/env bash

set -e  # exit on errors

[ -f .travis/.env ] && source .travis/.env

pip install --upgrade pip
pip install -r requirements.txt
pip install .
