import oyabun
from oyabun.version import verify_version


def test_version() -> None:
    assert oyabun.__version__ == "2022.12.12"


def test_verify_version() -> None:
    verify_version()
