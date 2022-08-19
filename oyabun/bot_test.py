import pytest

from oyabun.bot import Bot

pytestmark = [
    pytest.mark.asyncio,
]


async def test_answerCallbackQuery(test_bot: Bot) -> None:
    answered = await test_bot.answerCallbackQuery(
        callback_query_id="cbq",
    )

    assert answered


async def test_getMe(test_bot: Bot) -> None:
    me = await test_bot.getMe()

    assert me.id == 1
    assert me.is_bot is True
    assert me.first_name == "FN"
