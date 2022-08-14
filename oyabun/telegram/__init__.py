from typing import Type

from oyabun.telegram.base import __models__ as __models__base
from oyabun.telegram.base import Request
from oyabun.telegram.base import Response
from oyabun.telegram.base import ResponseParameters
from oyabun.telegram.base import TelegramBotApiType
from oyabun.telegram.entities import __models__ as __models__entities
from oyabun.telegram.entities import BotCommand
from oyabun.telegram.entities import BotCommandScope
from oyabun.telegram.entities import BotCommandScopeDefault
from oyabun.telegram.entities import CallbackQuery
from oyabun.telegram.entities import Chat
from oyabun.telegram.entities import ChatLocation
from oyabun.telegram.entities import ChatPermissions
from oyabun.telegram.entities import ChatPhoto
from oyabun.telegram.entities import File
from oyabun.telegram.entities import ForceReply
from oyabun.telegram.entities import InlineKeyboardButton
from oyabun.telegram.entities import InlineKeyboardMarkup
from oyabun.telegram.entities import KeyboardButton
from oyabun.telegram.entities import Location
from oyabun.telegram.entities import Message
from oyabun.telegram.entities import MessageEntity
from oyabun.telegram.entities import PhotoSize
from oyabun.telegram.entities import ReplyKeyboardMarkup
from oyabun.telegram.entities import ReplyKeyboardRemove
from oyabun.telegram.entities import Update
from oyabun.telegram.entities import User
from oyabun.telegram.entities import WebhookInfo
from oyabun.telegram.requests import __models__ as __models__requests
from oyabun.telegram.requests import AnswerCallbackQueryRequest
from oyabun.telegram.requests import DeleteWebhookRequest
from oyabun.telegram.requests import GetChatRequest
from oyabun.telegram.requests import GetFileRequest
from oyabun.telegram.requests import GetMeRequest
from oyabun.telegram.requests import GetUpdatesRequest
from oyabun.telegram.requests import GetWebhookInfoRequest
from oyabun.telegram.requests import SendMessageRequest
from oyabun.telegram.requests import SendPhotoRequest
from oyabun.telegram.requests import SetWebhookRequest
from oyabun.telegram.responses import __models__ as __models__responses
from oyabun.telegram.responses import AnswerCallbackQueryResponse
from oyabun.telegram.responses import DeleteWebhookResponse
from oyabun.telegram.responses import GetChatResponse
from oyabun.telegram.responses import GetFileResponse
from oyabun.telegram.responses import GetMeResponse
from oyabun.telegram.responses import GetUpdatesResponse
from oyabun.telegram.responses import GetWebhookInfoResponse
from oyabun.telegram.responses import SendMessageResponse
from oyabun.telegram.responses import SendPhotoResponse
from oyabun.telegram.responses import SetWebhookResponse

__models__: set[Type[TelegramBotApiType]] = (
    __models__base
    | __models__entities  # noqa: W503
    | __models__requests  # noqa: W503
    | __models__responses  # noqa: W503
)

for _model in __models__:
    _model.update_forward_refs()

__all__ = (
    "AnswerCallbackQueryRequest",
    "AnswerCallbackQueryResponse",
    "BotCommand",
    "BotCommandScope",
    "BotCommandScopeDefault",
    "CallbackQuery",
    "Chat",
    "ChatLocation",
    "ChatPermissions",
    "ChatPhoto",
    "DeleteWebhookRequest",
    "DeleteWebhookResponse",
    "File",
    "ForceReply",
    "GetChatRequest",
    "GetChatResponse",
    "GetFileRequest",
    "GetFileResponse",
    "GetMeRequest",
    "GetMeResponse",
    "GetUpdatesRequest",
    "GetUpdatesResponse",
    "GetWebhookInfoRequest",
    "GetWebhookInfoResponse",
    "InlineKeyboardButton",
    "InlineKeyboardMarkup",
    "KeyboardButton",
    "Location",
    "Message",
    "MessageEntity",
    "PhotoSize",
    "ReplyKeyboardMarkup",
    "ReplyKeyboardRemove",
    "Request",
    "Response",
    "ResponseParameters",
    "SendMessageRequest",
    "SendMessageResponse",
    "SendPhotoRequest",
    "SendPhotoResponse",
    "SetWebhookRequest",
    "SetWebhookResponse",
    "Update",
    "User",
    "WebhookInfo",
)
