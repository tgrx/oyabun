import asyncio
import os

from devtools import debug
from dotenv import load_dotenv

from oyabun.bot import Bot
from oyabun.samurai.fsm.machine import FSM
from oyabun.samurai.fsm import actions
from oyabun.samurai.persistence import Persistence
from oyabun.samurai.states import State

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN") or ""
assert token, "cannot start: TELEGRAM_BOT_TOKEN is not set"


async def main() -> None:
    bot = Bot(token)
    db = Persistence()
    fsm = FSM(db, bot)

    fsm.register(State.UNKNOWN)

    while True:
        print("\n", "-" * 30, "cycle", "-" * 30)  # noqa: T201

        offset = await db.load_updates_offset()
        debug(offset)

        updates = await bot.getUpdates(offset=offset, timeout=30)
        if not updates:
            continue

        for update in updates:
            await fsm.transit(update)

            offset = max(offset, update.update_id) + 1
            await db.store_updates_offset(offset)

        await asyncio.sleep(4)


if __name__ == "__main__":
    asyncio.run(main())
