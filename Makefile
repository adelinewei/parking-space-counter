install:
	pip install --upgrade pip && \
		pip install -r requirements-dev.txt

test:
	python -m pytest -vv --cov-report term-missing --cov=src tests

flake8:
	flake8 -v --exclude=*.pyc,__pycache__,.venv,.pytest_cache \
		--count --max-line-length=150 --ignore=E226,E231

picker:
	python src/parking_space_picker.py

start:
	python src/main.py


all: install flake8 test