from pathlib import Path

_this_file = Path(__file__).resolve()

DIR_SAMURAI = _this_file.parent.resolve()

DIR_REPO = DIR_SAMURAI.parent.resolve()

DIR_ARTIFACTS = (DIR_REPO / ".artifacts").resolve()

DIR_TMP = (DIR_REPO / "tmp").resolve()
