.PHONY: lint
lint:
	tox -e isort
	tox -e black

.PHONY: lint-check
lint-check:
	tox -e bandit
	tox -e safety
	tox -e black-check
	tox -e isort-check
	tox -e flake8