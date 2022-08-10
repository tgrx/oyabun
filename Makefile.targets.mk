.PHONY: build upload-test upload get-version clean clean-python clean-dist
.PHONY: format qa tests coverage code-typing code-format code-linters sh
.PHONY: venv-dir venv venv-dev venv-deploy venv-deploy-all upgrade-venv
.PHONY: verify-version


verify-version:
	$(call log, verify version consistency)
	python -m oyabun.version


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
	

format:
	$(call log, reorganizing imports & formatting code)
	isort --virtual-env="$(DIR_VENV)" \
		"$(DIR_SRC)" \
		|| exit 1
	black \
		"$(DIR_SRC)" \
		|| exit 1


qa: verify-version tests coverage code-typing code-format code-linters
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
		"$(DIR_SRC)" \
		|| exit 1
	black --check \
		"$(DIR_SRC)" \
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


venv-deploy:
	$(call log, installing packages into system)
	poetry install
