#!/usr/bin/env bash

# without parameters - runs the entire test suite
# $ bin/run_tests.sh

# running an individual test:
# $ bin/run_tests.sh knesset_data.dataservice.tests.committees.test_committees

# you can pass any parameter, see the help message:
# $ bin/run_tests.sh --help

python -m unittest ${*:-discover -v}
