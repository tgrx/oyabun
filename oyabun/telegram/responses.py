from typing import Optional
from typing import Type

from pydantic import Field

from oyabun.telegram import File
from oyabun.telegram.base import Response
from oyabun.telegram.entities import Chat
from oyabun.telegram.entities import Message
from oyabun.telegram.entities import Update
from oyabun.telegram.entities import User
from oyabun.telegram.entities import WebhookInfo


class AnswerCallbackQueryResponse(Response[bool]):
    result: bool = Field(False)


class DeleteWebhookResponse(Response[bool]):
    result: bool = Field(False)


class EditMessageCaptionResponse(Response[bool | Message]):
    result: Optional[bool | Message] = Field(None)


class EditMessageReplyMarkupResponse(Response[bool | Message]):
    result: Optional[bool | Message] = Field(None)


class EditMessageTextResponse(Response[bool | Message]):
    result: Optional[bool | Message] = Field(None)


class GetChatResponse(Response[Chat]):
    result: Optional[Chat] = Field(None)


class GetFileResponse(Response[File]):
    result: Optional[File] = Field(None)


class GetMeResponse(Response[User]):
    result: Optional[User] = Field(None)


class GetUpdatesResponse(Response[list[Update]]):
    result: list[Update] = Field(default_factory=list)


class GetWebhookInfoResponse(Response[WebhookInfo]):
    result: Optional[WebhookInfo] = Field(None)


class SendMessageResponse(Response[Message]):
    result: Optional[Message] = Field(None)


class SendPhotoResponse(Response[Message]):
    result: Optional[Message] = Field(None)


class SetWebhookResponse(Response[bool]):
    result: bool = Field(False)


__models__: set[Type[Response]] = {
    AnswerCallbackQueryResponse,
    DeleteWebhookResponse,
    EditMessageCaptionResponse,
    EditMessageReplyMarkupResponse,
    EditMessageTextResponse,
    GetChatResponse,
    GetFileResponse,
    GetMeResponse,
    GetUpdatesResponse,
    GetWebhookInfoResponse,
    SendMessageResponse,
    SendPhotoResponse,
    SetWebhookResponse,
}

__all__ = (
    "__models__",
    "AnswerCallbackQueryResponse",
    "DeleteWebhookResponse",
    "EditMessageCaptionResponse",
    "EditMessageReplyMarkupResponse",
    "EditMessageTextResponse",
    "GetChatResponse",
    "GetFileResponse",
    "GetMeResponse",
    "GetUpdatesResponse",
    "GetWebhookInfoResponse",
    "SendMessageResponse",
    "SendPhotoResponse",
    "SetWebhookResponse",
)
