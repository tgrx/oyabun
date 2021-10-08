from consigliere.scheme.entities import File, InputFile, Message, MessageEntity, ReplyMarkupType
from typing import List, Optional
from typing import Union

from consigliere.scheme import GetMeResponse
from consigliere.scheme import User
from consigliere.scheme.base import Request
from consigliere.scheme.base import Response


def prepare_request() -> None:
    pass


async def call_api(method: str, request: Request) -> Response:
    return Response(ok=True)


async def getMe() -> User:
    """
    A simple method for testing your bot's auth token.
    Requires no parameters.
    Returns basic information about the bot in form of a User object.
    """

    req = prepare_request()
    resp: GetMeResponse = await call_api("getMe", req)
    return resp.result


async def sendMessage(
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,  # TODO: add as enum: https://core.telegram.org/bots/api#formatting-options
        entities: Optional[List[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[ReplyMarkupType] = None,
) -> Message:
    return Message()


async def sendPhoto(
    chat_id: Union[int, str],
    photo: InputFile,  # The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20
    caption: Optional[str] = None,  # 0-1024
    parse_mode: Optional[str] = None,  # TODO: add as enum: https://core.telegram.org/bots/api#formatting-options
    caption_entities: Optional[List[MessageEntity]] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    allow_sending_without_reply: Optional[bool] = None,
    reply_markup: Optional[ReplyMarkupType] = None,
) -> Message:
    """
    29    response = requests.post(
    30         f"{BOT_URL}/sendPhoto",
    31         data={"chat_id": request.chat_id, "caption": "Processed",},
    32         files={"photo": ("InputFile", processed_photo)},
    33     )
    """
    return Message()


async def sendChatAction(
    chat_id: Union[int, str],
    action: str,  # TODO: enum https://core.telegram.org/bots/api#sendchataction
) -> bool:
    return False


async def getFile(
    file_id: str,
) -> File:
    """
    Note: This function may not preserve the original file name and MIME type.
    You should save the file's MIME type and name (if available) when the File object is received.
    """
    return File()


async def setMyCommands(
    commands: List[BotCommand],
    scope: Optional[BotCommandScope] = None,
    language_code: Optional[str] = None,  # A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
) -> bool:
    # TODO: https://core.telegram.org/bots#commands
    # TODO: https://core.telegram.org/bots/api#setmycommands
    return False


async def deleteMyCommands(
    scope: Optional[BotCommandScope] = None,
    language_code: Optional[str] = None,  # A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
) -> bool:
    # TODO: https://core.telegram.org/bots/api#deletemycommands
    return False


async def getMyCommands(
    scope: Optional[BotCommandScope] = None,
    language_code: Optional[str] = None,  # A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
) -> bool:
    return False



# TODO: local method:
#       - pack params into an object of subclass of Request
#       - call api with actual method name and request
#       - get a response / error
# RESOLVED: how to deal with null request? -- as no params
# RESOLVED: how to deal with invalid request params? -- validate with Pydantic
# RESOLVED: how to deal with error response? -- raise an Exception and fuck off
# TODO: check specific methods like send files, photos etc - req/resp may vary - requests.post(files={...})
