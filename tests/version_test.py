import oyabun
from oyabun.version import verify_version


def test_version() -> None:
    assert oyabun.__version__ == "2025.4.20"


def test_verify_version() -> None:
    verify_version()
