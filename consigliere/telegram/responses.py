from typing import Optional
from typing import Set
from typing import Type

from pydantic import Field

from consigliere.telegram import File
from consigliere.telegram.base import Response
from consigliere.telegram.entities import Message
from consigliere.telegram.entities import User
from consigliere.telegram.entities import WebhookInfo


class GetFileResponse(Response[File]):
    result: Optional[File] = Field(None)


class GetMeResponse(Response[User]):
    result: Optional[User] = Field(None)


class GetWebhookInfoResponse(Response[WebhookInfo]):
    result: Optional[WebhookInfo] = Field(None)


class SendMessageResponse(Response[Message]):
    result: Optional[Message] = Field(None)


class SendPhotoResponse(Response[Message]):
    result: Optional[Message] = Field(None)


class SetWebhookResponse(Response[bool]):
    result: bool = Field(False)


class DeleteWebhookResponse(Response[bool]):
    result: bool = Field(False)


__models__: Set[Type[Response]] = {
    DeleteWebhookResponse,
    GetFileResponse,
    GetMeResponse,
    GetWebhookInfoResponse,
    SendMessageResponse,
    SendPhotoResponse,
    SetWebhookResponse,
}

__all__ = (
    "__models__",
    "DeleteWebhookResponse",
    "GetFileResponse",
    "GetMeResponse",
    "GetWebhookInfoResponse",
    "SendMessageResponse",
    "SendPhotoResponse",
    "SetWebhookResponse",
)
