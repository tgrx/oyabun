from collections.abc import Generator
from collections.abc import Iterator
from collections.abc import Mapping
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from typing import IO
from typing import Any
from typing import Generic
from typing import TypeVar


class TelegramBotApiType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        serialize_by_alias=True,
        strict=False,
        validate_assignment=True,
        validate_default=True,
    )

    def _prepare_export_kw(
        self,
        kwargs: Mapping[str, Any],
        /,
    ) -> Mapping[str, Any]:
        new_kwargs: Mapping[str, Any] = kwargs | {  # type: ignore[operator]
            "exclude_none": True,
            "exclude_unset": True,
        }

        return new_kwargs

    def model_dump(self, /, **kwargs: Any) -> dict[str, Any]:
        kw = self._prepare_export_kw(kwargs)
        return super().model_dump(**kw)

    def model_dump_json(self, /, **kwargs: Any) -> str:
        kw = self._prepare_export_kw(kwargs)
        return super().model_dump_json(**kw)

    def model_dump_jsonb(self, /, **kwargs: Any) -> bytes:
        return self.model_dump_json(**kwargs).encode("utf-8")


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

    def _prepare_export_kw(
        self, kw: Mapping[str, Any], /
    ) -> Mapping[str, Any]:
        new_kw: Mapping[str, Any] = kw | {  # type: ignore[operator]
            "exclude": frozenset(self._get_input_files()),
        }
        return super()._prepare_export_kw(new_kw)


class ResponseParameters(TelegramBotApiType):
    migrate_to_chat_id: None | int = Field(None)
    retry_after: None | int = Field(None)


ResponseResultT = TypeVar("ResponseResultT")


class Response(TelegramBotApiType, Generic[ResponseResultT]):
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

    description: None | str = None
    error_code: None | int = None
    ok: bool
    parameters: None | ResponseParameters = None
    result: None | ResponseResultT = None


BaseModelType = type[BaseModel]

__models__: set[type[TelegramBotApiType]] = {
    Request,
    Response,
    ResponseParameters,
    TelegramBotApiType,
}
