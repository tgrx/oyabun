from typing import Optional

from pydantic import Field

from .base import Response
from .entities import Message
from .entities import User
from .entities import WebhookInfo


class GetMeResponse(Response):
    """
    Returns basic information about the bot in form of a User object.
    https://core.telegram.org/bots/api#getme
    """

    result: Optional[User] = Field(None)


class GetWebhookInfoResponse(Response):
    """
    On success, returns a WebhookInfo object.
    If the bot is using getUpdates,
        will return an object with the url field empty.
    https://core.telegram.org/bots/api#getwebhookinfo
    """

    result: Optional[WebhookInfo] = Field(None)


class SetWebhookResponse(Response):
    """
    Returns True on success.
    https://core.telegram.org/bots/api#setwebhook
    """

    result: bool = Field(False)


class SendMessageResponse(Response):
    """
    On success, the sent Message is returned.
    https://core.telegram.org/bots/api#sendmessage
    """

    result: Optional[Message] = Field(None)


__all__ = (
    GetMeResponse.__name__,
    GetWebhookInfoResponse.__name__,
    SendMessageResponse.__name__,
    SetWebhookResponse.__name__,
)
