from typing import Any
from typing import Optional
from typing import Type
from typing import Union

from pydantic import Field

from oyabun.telegram.base import Request
from oyabun.telegram.entities import InlineKeyboardMarkup
from oyabun.telegram.entities import MessageEntity
from oyabun.telegram.entities import ReplyMarkupType


class AnswerCallbackQueryRequest(Request):
    cache_time: Optional[int] = Field(None)
    callback_query_id: str = Field(...)
    show_alert: Optional[bool] = Field(None)
    text: Optional[str] = Field(None)
    url: Optional[str] = Field(None)


class DeleteWebhookRequest(Request):
    drop_pending_updates: Optional[bool] = Field(None)


class EditMessageTextRequest(Request):
    chat_id: Optional[Union[int, str]] = Field(None)
    disable_web_page_preview: Optional[bool] = Field(None)
    entities: Optional[list[MessageEntity]] = Field(None)
    inline_message_id: Optional[str] = Field(None)
    message_id: Optional[int] = Field(None)
    parse_mode: Optional[str] = Field(None)
    reply_markup: Optional[InlineKeyboardMarkup] = Field(None)
    text: str = Field(...)


class GetChatRequest(Request):
    chat_id: Union[int, str] = Field(...)


class GetFileRequest(Request):
    file_id: str = Field(...)


class GetMeRequest(Request):
    pass


class GetUpdatesRequest(Request):
    allowed_updates: Optional[list[str]] = Field(None)
    limit: Optional[int] = Field(None, le=100, ge=1)
    offset: Optional[int] = Field(None)
    timeout: Optional[int] = Field(None, ge=0)


class GetWebhookInfoRequest(Request):
    pass


class SendMessageRequest(Request):
    allow_sending_without_reply: Optional[bool] = Field(None)
    chat_id: Union[int, str] = Field(...)
    disable_notification: Optional[bool] = Field(None)
    disable_web_page_preview: Optional[bool] = Field(None)
    entities: Optional[list[MessageEntity]] = Field(None)
    parse_mode: Optional[str] = Field(None)
    reply_markup: Optional[ReplyMarkupType] = Field(None)
    reply_to_message_id: Optional[int] = Field(None)
    text: str = Field(...)


class SendPhotoRequest(Request):
    allow_sending_without_reply: Optional[bool] = Field(None)
    caption: Optional[str] = Field(None)
    caption_entities: Optional[list[MessageEntity]] = Field(None)
    chat_id: Union[int, str] = Field(...)
    disable_notification: Optional[bool] = Field(None)
    parse_mode: Optional[str] = Field(None)
    photo: Any = Field(...)
    reply_markup: Optional[ReplyMarkupType] = Field(None)
    reply_to_message_id: Optional[int] = Field(None)


class SetWebhookRequest(Request):
    allowed_updates: Optional[list[str]] = Field(None)
    certificate: Any = Field(None)
    drop_pending_updates: Optional[bool] = Field(None)
    ip_address: Optional[str] = Field(None)
    max_connections: Optional[int] = Field(None)
    url: str = Field(...)


__models__: set[Type[Request]] = {
    AnswerCallbackQueryRequest,
    DeleteWebhookRequest,
    EditMessageTextRequest,
    GetChatRequest,
    GetFileRequest,
    GetMeRequest,
    GetUpdatesRequest,
    GetWebhookInfoRequest,
    SendMessageRequest,
    SendPhotoRequest,
    SetWebhookRequest,
}

__all__ = (
    "__models__",
    "AnswerCallbackQueryRequest",
    "DeleteWebhookRequest",
    "EditMessageTextRequest",
    "GetChatRequest",
    "GetFileRequest",
    "GetMeRequest",
    "GetUpdatesRequest",
    "GetWebhookInfoRequest",
    "SendMessageRequest",
    "SendPhotoRequest",
    "SetWebhookRequest",
)
