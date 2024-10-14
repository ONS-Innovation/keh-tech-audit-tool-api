.DEFAULT_GOAL := all

.PHONY: all
all: ## Show the available make targets.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: clean
clean:  ## Clean the temporary files
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .pytest_cache

.PHONY: format
format:  ## Format the code
	poetry run black .
	poetry run ruff check . --fix

.PHONY: black
black:  ## Run black
	poetry run black aws_lambda_script

.PHONY: ruff
ruff:  ## Run ruff
	poetry run ruff check aws_lambda_script --fix

.PHONY: pylint
pylint:  ## Run pylint
	poetry run pylint aws_lambda_script

.PHONY: lint
lint:  ## Run Python linter
	make black
	make ruff || true
	make pylint || true

.PHONY: mypy
mypy:  ## Run mypy
	poetry run mypy aws_lambda_script

.PHONY: install
install:  ## Install the dependencies excluding dev
	poetry install --only main --no-root

.PHONY: install-dev
install-dev:  ## Install the dependencies including dev
	poetry install --no-root

.PHONY: pytest
pytest:  ## Run pytest
	poetry run pytest