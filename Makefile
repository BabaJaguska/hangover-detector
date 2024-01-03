.PHONY: install format lint test help all

install:
	pip install -r requirements.txt

format:
	black --line-length=79 .

lint:
	flake8 --ignore=E501 .

test:
	pytest tests/

help:
	@echo "install - install dependencies"
	@echo "format - format code"
	@echo "lint - lint code"
	@echo "test - run tests"
	@echo "help - show this help message and exit"
	@echo "all - install, format, lint, test"

all: install format lint test
