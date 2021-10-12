from typing import Set
from typing import Type

from consigliere.telegram.base import __models__ as __models__base
from consigliere.telegram.base import Request
from consigliere.telegram.base import Response
from consigliere.telegram.base import ResponseParameters
from consigliere.telegram.base import TelegramBotApiType
from consigliere.telegram.entities import __models__ as __models__entities
from consigliere.telegram.entities import BotCommand
from consigliere.telegram.entities import BotCommandScope
from consigliere.telegram.entities import BotCommandScopeDefault
from consigliere.telegram.entities import Chat
from consigliere.telegram.entities import File
from consigliere.telegram.entities import ForceReply
from consigliere.telegram.entities import InlineKeyboardButton
from consigliere.telegram.entities import InlineKeyboardMarkup
from consigliere.telegram.entities import KeyboardButton
from consigliere.telegram.entities import Message
from consigliere.telegram.entities import MessageEntity
from consigliere.telegram.entities import ReplyKeyboardMarkup
from consigliere.telegram.entities import ReplyKeyboardRemove
from consigliere.telegram.entities import Update
from consigliere.telegram.entities import User
from consigliere.telegram.entities import WebhookInfo
from consigliere.telegram.requests import __models__ as __models__requests
from consigliere.telegram.requests import GetFileRequest
from consigliere.telegram.requests import SendMessageRequest
from consigliere.telegram.requests import SendPhotoRequest
from consigliere.telegram.responses import __models__ as __models__responses
from consigliere.telegram.responses import GetFileResponse
from consigliere.telegram.responses import GetMeResponse
from consigliere.telegram.responses import GetWebhookInfoResponse
from consigliere.telegram.responses import SendMessageResponse
from consigliere.telegram.responses import SendPhotoResponse
from consigliere.telegram.responses import SetWebhookResponse

__models__: Set[Type[TelegramBotApiType]] = (
    __models__base
    | __models__entities  # noqa: W503
    | __models__requests  # noqa: W503
    | __models__responses  # noqa: W503
)

for _model in __models__:
    _model.update_forward_refs()

__all__ = (
    "BotCommand",
    "BotCommandScope",
    "BotCommandScopeDefault",
    "Chat",
    "File",
    "ForceReply",
    "GetFileRequest",
    "GetFileResponse",
    "GetMeResponse",
    "GetWebhookInfoResponse",
    "InlineKeyboardButton",
    "InlineKeyboardMarkup",
    "KeyboardButton",
    "Message",
    "MessageEntity",
    "ReplyKeyboardMarkup",
    "ReplyKeyboardRemove",
    "Request",
    "Response",
    "ResponseParameters",
    "SendMessageRequest",
    "SendMessageResponse",
    "SendPhotoRequest",
    "SendPhotoResponse",
    "SetWebhookResponse",
    "Update",
    "User",
    "WebhookInfo",
)
