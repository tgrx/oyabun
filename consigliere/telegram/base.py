from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Generic
from typing import IO
from typing import Iterator
from typing import List
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from pydantic import BaseModel
from pydantic import Field


class TelegramBotApiType(BaseModel):
    """
    All types used in the Bot API responses are represented as JSON-objects.
    It is safe to use 32-bit signed integers
        for storing all Integer fields unless otherwise noted.
    Optional fields may be not returned when irrelevant.
    https://core.telegram.org/bots/api#available-types
    """

    def _prepare_export_kw(self, kw: Dict[str, Any]) -> None:
        kw["exclude_none"] = True
        kw["exclude_unset"] = True

    def json(self, **kw: Any) -> str:  # noqa: A003, VNE003
        self._prepare_export_kw(kw)
        return super().json(**kw)

    def dict(self, **kw: Any) -> Dict:  # noqa: A003, VNE003
        self._prepare_export_kw(kw)
        return super().dict(**kw)


class Request(TelegramBotApiType):
    def _get_input_files(self) -> Dict[str, Union[Path, IO]]:
        fields_values = (
            (attr, getattr(self, attr, None)) for attr in self.__fields__
        )

        fields_files = (
            field_value
            for field_value in fields_values
            if isinstance(field_value[1], (Path, BytesIO))
        )

        return dict(fields_files)

    def _prepare_export_kw(self, kw: Dict[str, Any]) -> None:
        kw["exclude"] = frozenset(self._get_input_files())
        return super()._prepare_export_kw(kw)

    @contextmanager
    def files(self) -> Iterator:
        opened_files: List[IO] = []

        def open_file(_path_or_io: Union[Path, IO]) -> IO:
            if isinstance(_path_or_io, BytesIO):
                return _path_or_io
            assert isinstance(_path_or_io, Path)
            _fp = _path_or_io.open("rb")
            opened_files.append(_fp)
            return _fp

        try:
            fields_file_tuples = {
                field: ("InputFile", open_file(value))
                for field, value in self._get_input_files().items()
            }

            yield fields_file_tuples
        finally:
            for _fp in opened_files:
                _fp.close()


class ResponseParameters(TelegramBotApiType):
    """
    Contains information about why a request was unsuccessful.
    https://core.telegram.org/bots/api#responseparameters
    """

    # fmt: off
    migrate_to_chat_id: Optional[int] = Field(None, description="Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.")
    retry_after: Optional[int] = Field(None, description="Optional. In case of exceeding flood control, the number of seconds left to wait before the request can be repeated")
    # fmt: on


ResponseResultT = TypeVar("ResponseResultT")


class Response(Generic[ResponseResultT], TelegramBotApiType):
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
    result: Optional[ResponseResultT] = Field(None)
    error_code: Optional[int] = Field(None)
    description: Optional[str] = Field(None)
    parameters: Optional[ResponseParameters] = Field(None)


BaseModelType = Type[BaseModel]

__models__: Set[Type[TelegramBotApiType]] = {
    Request,
    Response,
    ResponseParameters,
    TelegramBotApiType,
}

__all__ = (
    "__models__",
    "Request",
    "Response",
    "ResponseParameters",
    "TelegramBotApiType",
)
