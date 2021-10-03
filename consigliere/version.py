"""
https://www.python.org/dev/peps/pep-0440/
"""
import os
import re
from typing import Dict
from typing import Optional
from typing import TypeVar

from pydantic import BaseModel
from pydantic import Field
from pydantic import StrictInt
from pydantic import StrictStr


class NumericComponent(StrictInt):
    ge = 0


class LocalComponent(StrictStr):
    min_length = 0
    regex = re.compile(r"^[a-z0-9]{0,40}(?:[-_.][a-z0-9]{1,40}){0,4}$")
    strip_whitespace = True


class Version(BaseModel):
    """
    https://www.python.org/dev/peps/pep-0440/#version-scheme
    """

    epoch: NumericComponent = Field(...)
    major: NumericComponent = Field(...)
    minor: NumericComponent = Field(...)
    micro: NumericComponent = Field(...)
    a: Optional[NumericComponent] = Field(None)  # noqa: VNE001
    b: Optional[NumericComponent] = Field(None)  # noqa: VNE001
    rc: Optional[NumericComponent] = Field(None)  # noqa: VNE001
    post: Optional[NumericComponent] = Field(None)
    dev: Optional[NumericComponent] = Field(None)
    local: Optional[LocalComponent] = Field(None)

    _T = TypeVar("_T")
    _TV = Dict[str, _T]

    def __str__(self) -> str:
        epoch = "" if not self.epoch else f"{self.epoch}!"

        release = ".".join(map(str, (self.major, self.minor, self.micro)))

        alpha = "" if self.a is None else f"a{self.a}"
        beta = "" if self.b is None else f"b{self.b}"
        release_candidate = "" if self.rc is None else f"rc{self.rc}"
        pre = f"{alpha}{beta}{release_candidate}"

        post = "" if self.post is None else f".post{self.post}"

        dev = "" if self.dev is None else f".dev{self.dev}"

        local = "" if not self.local else f"+{self.local}"

        result = "".join(
            (
                epoch,
                release,
                pre,
                post,
                dev,
                local,
            )
        )

        return result


version = Version(
    epoch=0,
    major=0,
    minor=0,
    micro=1,
    a=7,
    b=None,
    rc=None,
    post=None,
    dev=None,
    local=os.getenv("CONSIGLIERE_VERSION_LOCAL"),
)

VERSION = str(version)
