from oyabun.telegram import File
from oyabun.telegram.base import Response
from oyabun.telegram.entities import ChatFullInfo
from oyabun.telegram.entities import Message
from oyabun.telegram.entities import Update
from oyabun.telegram.entities import User
from oyabun.telegram.entities import WebhookInfo
from pydantic import Field


class AnswerCallbackQueryResponse(Response[bool]):
    result: bool = Field(False)


class DeleteMessageResponse(Response[bool]):
    result: bool = Field(False)


class DeleteWebhookResponse(Response[bool]):
    result: bool = Field(False)


class EditMessageCaptionResponse(Response[bool | Message]):
    result: None | bool | Message = Field(None)


class EditMessageReplyMarkupResponse(Response[bool | Message]):
    result: None | bool | Message = Field(None)


class EditMessageTextResponse(Response[bool | Message]):
    result: None | bool | Message = Field(None)


class GetChatResponse(Response[ChatFullInfo]):
    result: None | ChatFullInfo = Field(None)


class GetFileResponse(Response[File]):
    result: None | File = Field(None)


class GetMeResponse(Response[User]):
    result: None | User = Field(None)


class GetUpdatesResponse(Response[list[Update]]):
    result: list[Update] = Field(default_factory=list)


class GetWebhookInfoResponse(Response[WebhookInfo]):
    result: None | WebhookInfo = Field(None)


class SendMessageResponse(Response[Message]):
    result: None | Message = Field(None)


class SendPhotoResponse(Response[Message]):
    result: None | Message = Field(None)


class SetWebhookResponse(Response[bool]):
    result: bool = Field(False)


__models__: set[type[Response]] = {
    AnswerCallbackQueryResponse,
    DeleteMessageResponse,
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
