install:
	pip install --upgrade pip && \
		pip install -r requirements-dev.txt

test:
	python -m pytest -vv --cov-report term-missing --cov=src tests

flake8:
	flake8 -v


all: install flake8 test