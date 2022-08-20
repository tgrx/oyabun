.PHONY: dist upload-test upload get-version clean clean-python clean-dist
.PHONY: format qa tests coverage code-typing code-format code-linters sh
.PHONY: venv-dir venv venv-dev venv-deploy venv-deploy-all upgrade-venv


get-version:
	@python -c "import oyabun; print(oyabun.__version__)"


clean: clean-python clean-dist
	$(call log, cleaning project)


clean-python:
	$(call log, cleaning python caches)
	rm -rf "$(DIR_ARTIFACTS)/coverage"
	rm -rf "$(DIR_ARTIFACTS)/mypy"
	rm -rf "$(DIR_ARTIFACTS)/pytest"


clean-dist:
	$(call log, cleaning distribution)
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/


dist: clean-dist
	$(call log, building distribution)
	poetry build --no-interaction


format:
	$(call log, reorganizing imports & formatting code)
	isort --virtual-env="$(DIR_VENV)" \
		"$(DIR_OYABUN)" \
		"$(DIR_SAMURAI)" \
		|| exit 1
	black \
		"$(DIR_OYABUN)" \
		"$(DIR_SAMURAI)" \
		|| exit 1


qa: tests coverage code-typing code-format code-linters
	$(call log, QA checks)


tests: clean-python
	$(call log, running tests)
	pytest


coverage:
	$(call log, calculating coverage)
	coverage html
	coverage xml


code-typing:
	$(call log, checking code typing)
	mypy


code-format:
	$(call log, checking code format)
	isort --virtual-env="$(DIR_VENV)" --check-only \
		"$(DIR_OYABUN)" \
		"$(DIR_SAMURAI)" \
		|| exit 1
	black --check \
		"$(DIR_OYABUN)" \
		"$(DIR_SAMURAI)" \
		|| exit 1


code-linters:
	$(call log, linting)
	flake8


sh:
	$(call log, starting Python shell)
	ipython


venv:
	$(call log, installing packages)
	poetry env use "$(shell cat .python-version)"
	poetry install --no-root
