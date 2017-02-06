#!/usr/bin/env bash

set -e  # exit on errors

pip install --upgrade pip
pip install -r requirements.txt
pip install .
