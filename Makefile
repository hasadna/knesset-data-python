.PHONY: install test

install:
	pip install -e .[develop]

test:
	tox
