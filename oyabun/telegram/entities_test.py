from datetime import datetime

from oyabun.telegram import Chat
from oyabun.telegram import InlineKeyboardButton
from oyabun.telegram import InlineKeyboardMarkup
from oyabun.telegram import KeyboardButton
from oyabun.telegram import Message
from oyabun.telegram import ReplyKeyboardMarkup
from oyabun.telegram import SendMessageRequest
from oyabun.telegram import User


def test_update_message_from_1() -> None:
    msg = Message(
        message_id=1,
        date="2020-10-23T13:12:11Z",  # type: ignore
        chat=Chat(id=1, type="t"),
        from_=User(id=1, is_bot=True, first_name="fn"),
    )

    assert msg.message_id == 1

    assert isinstance(msg.date, datetime)
    assert msg.date.year == 2020
    assert msg.date.month == 10
    assert msg.date.day == 23
    assert msg.date.hour == 13
    assert msg.date.minute == 12
    assert msg.date.second == 11

    assert msg.chat.id == 1

    assert isinstance(msg.from_, User)
    assert msg.from_.id == 1
    assert msg.from_.is_bot is True
    assert msg.from_.first_name == "fn"


def test_update_message_from_2() -> None:
    user = User(id=1, is_bot=True, first_name="fn")

    msg1 = Message(
        message_id=1,
        date="2020-10-23T13:12:11Z",  # type: ignore
        chat=Chat(id=1, type="t"),
        from_=user,
    )
    msg2 = Message(
        message_id=2,
        date="2020-01-02T03:04:05Z",  # type: ignore
        chat=Chat(id=1, type="t"),
        **{"from": user},  # type: ignore
    )

    d1 = msg1.dict()
    d2 = msg2.dict()

    assert d1["from"] == d2["from"]


def test_reply_markup() -> None:
    reply_markup_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="InlineKeyboardButton text",
                    callback_data="callback-data",
                ),
            ],
        ],
    )

    reply_markup_reply = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="KeyboardButton text",
                ),
            ],
        ],
    )

    request_inline = SendMessageRequest(
        chat_id=1,
        reply_markup=reply_markup_inline,
        text="2",
    )

    request_reply = SendMessageRequest(
        chat_id=1,
        reply_markup=reply_markup_reply,
        text="2",
    )

    dct = request_inline.dict()
    reply_markup = dct.get("reply_markup")
    assert reply_markup

    dct = request_reply.dict()
    reply_markup = dct.get("reply_markup")
    assert reply_markup


if __name__ == "__main__":
    test_reply_markup()
