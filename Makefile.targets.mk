.PHONY: build upload-test upload get-version clean clean-python clean-dist
.PHONY: format qa tests coverage code-typing code-format code-linters sh
.PHONY: venv-dir venv venv-dev venv-deploy venv-deploy-all upgrade-venv


build: clean
	$(call log, building wheels and bdist)
	python -m build --sdist --wheel --outdir dist/ .


upload-test: build
	$(call log, uploading dist to test.pypi.org)
	python -m twine upload --repository testpypi dist/*


upload: build
	$(call log, uploading dist to pypi.org)
	python -m twine upload dist/*


get-version:
	@python -c "from consigliere import __version__ as v; print(v.__version__)"


clean: clean-python clean-dist
	$(call log, cleaning project)


clean-python:
	$(call log, cleaning python caches)
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf coverage.xml
	rm -rf htmlcov/


clean-dist:
	$(call log, cleaning distribution)
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/
	

format:
	$(call log, reorganizing imports & formatting code)
	isort --virtual-env="$(DIR_VENV)" \
		"$(DIR_SRC)" \
		"$(DIR_TESTS)" \
		|| exit 1
	black \
		"$(DIR_SRC)" \
		"$(DIR_TESTS)" \
		|| exit 1


qa: tests coverage code-typing code-format code-linters
	$(call log, QA checks)


tests: clean-python
	$(call log, running tests)
	python -m pytest


coverage:
	$(call log, calculating coverage)
	coverage html
	coverage xml


code-typing:
	$(call log, checking code typing)
	python -m mypy


code-format:
	$(call log, checking code format)
	isort --virtual-env="$(DIR_VENV)" --check-only \
		"$(DIR_SRC)" \
		"$(DIR_TESTS)" \
		|| exit 1
	black --check \
		"$(DIR_SRC)" \
		"$(DIR_TESTS)" \
		|| exit 1


code-linters:
	$(call log, linting)
	python -m flake8


sh:
	$(call log, starting Python shell)
	ipython


venv-dir:
	$(call log, initializing venv directory)
	test -d .venv || mkdir .venv


venv: venv-dir
	$(call log, installing packages)
	pipenv install


venv-dev: venv-dir
	$(call log, installing development packages)
	pipenv install --dev


venv-deploy: venv-dir
	$(call log, installing packages into system)
	pipenv install --deploy --system


venv-deploy-all: venv-dir
	$(call log, installing all packages into system)
	pipenv install --dev --deploy --system


upgrade-venv: venv-dir
	$(call log, upgrading all packages in virtualenv)
	pipenv update --dev
