import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from aiohttp.test_utils import TestServer

from oyabun.bot import Bot
from oyabun.bot_test_app import TelegramApp


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
async def test_bot() -> AsyncGenerator[Bot, None]:
    tg = TelegramApp()
    server: TestServer = TestServer(tg)
    await server.start_server()

    bot = Bot(token=tg.get_telegram_bot_api_token())
    bot.TELEGRAM_BOT_API_URL = str(server.make_url(""))

    yield bot

    await server.close()
