from oyabun.telegram import Chat
from oyabun.telegram import Message
from oyabun.telegram import User


def test_update_message_from() -> None:
    msg = Message(
        message_id=1,
        date="2020-01-01T00:00:00Z",
        chat=Chat(id=1),
        from_=User(id=1, is_bot=True, first_name="fn"),
    )

    assert msg.from_ is not None
