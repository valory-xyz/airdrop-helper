.PHONY: lint
formatters:
	tox -e isort
	tox -e black

.PHONY: lint-check
all-linters:
	tox -e bandit
	tox -e safety
	tox -e black-check
	tox -e isort-check
	tox -e flake8
	tox -e darglint
	tox -e pylint
	tox -e mypy