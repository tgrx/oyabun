from typing import NamedTuple


class VersionTuple(NamedTuple):
    major: int = 2022
    minor: int = 8
    micro: int = 20

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.micro}"


version = VersionTuple()

VERSION = str(version)


def verify_version() -> None:
    # keep it here, dev functional, until py 3.10
    from pathlib import Path

    import toml

    this_file = Path(__file__)
    repo = this_file.parent.parent.resolve()
    pyproject_toml = repo / "pyproject.toml"
    assert pyproject_toml.is_file()
    with pyproject_toml.open("r") as stream:
        data = toml.load(stream)
    version_pyproject_toml = (
        data.get("tool", {}).get("poetry", {}).get("version")
    )

    err = (
        f"incorrect versions: "
        f"{version_pyproject_toml!r} (in pyproject.toml) "
        f"!= {VERSION!r} (in {this_file.as_posix()})"
    )
    assert version_pyproject_toml == VERSION, err
