from typing import Any
from typing import Dict
from typing import Optional
from typing import Type

from pydantic import BaseModel
from pydantic import ConstrainedStr
from pydantic import Field


class TelegramBotApiType(BaseModel):
    """
    All types used in the Bot API responses are represented as JSON-objects.
    It is safe to use 32-bit signed integers
        for storing all Integer fields unless otherwise noted.
    Optional fields may be not returned when irrelevant.
    https://core.telegram.org/bots/api#available-types
    """

    def json(self, **kw: Any) -> str:  # noqa: A003, VNE003
        kw["exclude_unset"] = True
        return super().json(**kw)

    def dict(self, **kw: Any) -> Dict:  # noqa: A003, VNE003
        kw["exclude_unset"] = True
        return super().dict(**kw)


class Request(TelegramBotApiType):
    pass


class ResponseParameters(TelegramBotApiType):
    """
    Contains information about why a request was unsuccessful.
    https://core.telegram.org/bots/api#responseparameters
    """

    # fmt: off
    migrate_to_chat_id: Optional[int] = Field(None, description="Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.")
    retry_after: Optional[int] = Field(None, description="Optional. In case of exceeding flood control, the number of seconds left to wait before the request can be repeated")
    # fmt: on


class Response(TelegramBotApiType):
    """
    The response contains a JSON object,
        which always has a Boolean field 'ok'
        and may have an optional String field 'description'
        with a human-readable description of the result.
    If 'ok' equals true, the request was successful
        and the result of the query can be found
        in the 'result' field.
    In case of an unsuccessful request,
        'ok' equals false and the error is explained
        in the 'description'.
    An Integer 'error_code' field is also returned,
        but its contents are subject to change in the future.
    Some errors may also have an optional field 'parameters'
        of the type ResponseParameters,
        which can help to automatically handle the error.
    https://core.telegram.org/bots/api#making-requests
    """

    ok: bool = Field(...)
    result: Any = Field(None)
    error_code: Optional[int] = Field(None)
    description: Optional[str] = Field(None)
    parameters: Optional[ResponseParameters] = Field(None)


BaseModelType = Type[BaseModel]


def update_forward_refs(klass: BaseModelType) -> BaseModelType:
    klass.update_forward_refs()
    return klass


class Str64(ConstrainedStr):
    min_length = 1
    max_length = 64


__all__ = (
    ResponseParameters.__name__,
    Str64.__name__,
    TelegramBotApiType.__name__,
    update_forward_refs.__name__,
)
