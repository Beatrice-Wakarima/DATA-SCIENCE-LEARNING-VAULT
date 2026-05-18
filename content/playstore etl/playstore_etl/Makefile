# Makefile for Google Play Store ETL Pipeline

.PHONY: help install test clean run lint format

help:
	@echo "Google Play Store ETL Pipeline - Available Commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run the ETL pipeline"
	@echo "  make clean      - Clean generated files"
	@echo "  make lint       - Run code linting"
	@echo "  make format     - Format code with black"
	@echo "  make setup-dev  - Setup development environment"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

test-verbose:
	pytest tests/ -vv --cov=src --cov-report=html

run:
	cd src && python pipeline.py

extract:
	cd src && python extract.py

transform:
	cd src && python transform.py

load:
	cd src && python load.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/

lint:
	flake8 src/ --max-line-length=100 --ignore=E203,W503
	pylint src/ --max-line-length=100

format:
	black src/ tests/ --line-length=100

setup-dev:
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  (Linux/Mac)"
	@echo "  venv\\Scripts\\activate     (Windows)"
