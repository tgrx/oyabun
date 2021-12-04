# Welcome to Consigliere contributing guide

## Development

To start a new feature/bugfix, one MUST create a new branch and a PR `<branch>` -> `main` for that.

## CI

A `development` workflow is for testing your code.

The `release` workflow is for deployment.

One MUST add a tag named `release-<version>`, push the tag and then the release will be deployed to PyPI.

A version must be equal to those in [consigliere/version.py](consigliere/version.py).
