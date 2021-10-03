from typing import List
from typing import Optional
from typing import Union

from pydantic import Field

from .base import Request
from .entities import ReplyMarkupType


class SendMessageRequest(Request):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    https://core.telegram.org/bots/api#sendmessage
    """

    # fmt: off
    chat_id: Union[int, str] = Field(..., description="Unique identifier for the target chat or username of the target channel (in the format @channelusername)")
    text: str = Field(..., description="Text of the message to be sent, 1-4096 characters after entities parsing")
    parse_mode: Optional[str] = Field(None, description="Mode for parsing entities in the message text. See formatting options for more details.")
    entities: List[str] = Field(default_factory=list, description="List of special entities that appear in message text, which can be specified instead of parse_mode")
    disable_web_page_preview: bool = Field(False, description="Disables link previews for links in this message")
    disable_notification: bool = Field(False, description="Sends the message silently. Users will receive a notification with no sound.")
    reply_to_message_id: Optional[int] = Field(None, description="If the message is a reply, ID of the original message")
    allow_sending_without_reply: bool = Field(False, description="Pass True, if the message should be sent even if the specified replied-to message is not found")
    reply_markup: Optional[ReplyMarkupType] = Field(None, description="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.")
    # fmt: on


__all__ = (SendMessageRequest.__name__,)
