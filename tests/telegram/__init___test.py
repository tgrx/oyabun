from oyabun.telegram.base import TelegramBotApiType


def test_photosize_importable_from_pkg() -> None:
    from oyabun import telegram

    obj = getattr(telegram, "PhotoSize", None)
    assert obj is not None
    assert issubclass(obj, TelegramBotApiType)
