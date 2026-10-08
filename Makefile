.PHONY: build check test
PYTHON ?= python3

build:
	$(PYTHON) scripts/build.py

check:
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/build.py --check

test:
	$(PYTHON) -m unittest discover -s tests -v
