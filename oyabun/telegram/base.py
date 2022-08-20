from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from typing import Any
from typing import Generator
from typing import Generic
from typing import IO
from typing import Iterator
from typing import Type
from typing import TypeVar

import orjson
from pydantic import BaseModel
from pydantic import Field


def orjson_dumps(value: Any, *, default: Any) -> str:
    return orjson.dumps(value, default=default).decode()


class TelegramBotApiType(BaseModel):
    class Config:
        allow_population_by_field_name = True
        extra = "forbid"
        json_dumps = orjson_dumps
        json_loads = orjson.loads

    def _prepare_export_kw(self, kw: dict[str, Any]) -> None:
        kw.update(
            {
                "by_alias": True,
                "exclude_none": True,
                "exclude_unset": True,
            }
        )

    def jsonb(self, **kw: Any) -> bytes:  # noqa: A003, VNE003
        value = self.json(**kw)
        if isinstance(value, bytes):
            return value

        return value.encode()

    def json(self, **kw: Any) -> str:  # noqa: A003, VNE003
        self._prepare_export_kw(kw)

        value: str | bytes = super().json(**kw)
        if isinstance(value, str):
            return value

        return value.decode()

    def dict(self, **kw: Any) -> dict:  # noqa: A003, VNE003
        self._prepare_export_kw(kw)
        return super().dict(**kw)


class Request(TelegramBotApiType):
    @contextmanager
    def files(self) -> Iterator[dict[str, IO]]:
        opened_files: list[IO] = []

        def open_file(_path_or_io: Path | IO) -> IO:
            if isinstance(_path_or_io, BytesIO):
                return _path_or_io
            assert isinstance(_path_or_io, Path)
            _fp = _path_or_io.open("rb")
            opened_files.append(_fp)
            return _fp

        try:
            fields_streams = {
                field: open_file(value)
                for field, value in self._get_input_files().items()
            }

            yield fields_streams
        finally:
            for fp in opened_files:
                fp.close()

    def _get_input_files(self) -> dict[str, Path | IO]:
        fields_values: Generator[tuple[str, Any], None, None] = (
            (attr, getattr(self, attr, None)) for attr in self.__fields__
        )

        fields_files: Generator[tuple[str, Path | IO], None, None] = (
            field_value
            for field_value in fields_values
            if isinstance(field_value[1], (Path, BytesIO))
        )

        return dict(fields_files)

    def _prepare_export_kw(self, kw: dict[str, Any]) -> None:
        kw["exclude"] = frozenset(self._get_input_files())
        return super()._prepare_export_kw(kw)


class ResponseParameters(TelegramBotApiType):
    migrate_to_chat_id: None | int = Field(None)
    retry_after: None | int = Field(None)


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
    result: None | ResponseResultT = Field(None)
    error_code: None | int = Field(None)
    description: None | str = Field(None)
    parameters: None | ResponseParameters = Field(None)


BaseModelType = Type[BaseModel]

__models__: set[Type[TelegramBotApiType]] = {
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
