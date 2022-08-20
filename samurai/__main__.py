import asyncio
import os

from devtools import debug
from dotenv import load_dotenv

from oyabun.bot import Bot
from samurai.fsm import actions
from samurai.fsm.machine import FSM
from samurai.persistence import Persistence
from samurai.states import State

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN") or ""
assert token, "cannot start: TELEGRAM_BOT_TOKEN is not set"

graph = (
    (
        State.NOT_STARTED,
        State.WAIT_FOR_PLAIN_TEXT,
        actions.Start,
    ),
    (
        State.WAIT_FOR_PLAIN_TEXT,
        State.WAIT_FOR_EDITING_TEXT,
        actions.RespondToPlainText,
    ),
    (
        State.WAIT_FOR_EDITING_TEXT,
        State.SEND_PHOTO,
        actions.RespondToEditingText,
    ),
    (
        State.SEND_PHOTO,
        State.WAIT_FOR_PHOTO,
        actions.SendPhoto,
    ),
    (
        State.WAIT_FOR_PHOTO,
        State.FINISHED,
        actions.ReplyWithProcessedPhoto,
    ),
    (
        State.FINISHED,
        State.NOT_STARTED,
        actions.Restart,
    ),
)


async def main() -> None:
    bot = Bot(token)
    db = Persistence()
    fsm = FSM(db, bot)

    for state0, state1, action_cls in graph:
        # TODO: un-ignore when this is resolved:  # noqa: T101
        # https://github.com/python/mypy/issues/5374
        fsm.register(state0, state1, action_cls)  # type: ignore

    async with bot.client_session():
        while True:
            print("\n", "-" * 30, "cycle", "-" * 30)  # noqa: T201

            offset = await db.load_updates_offset()
            debug(offset)

            updates = await bot.getUpdates(offset=offset, timeout=30)
            if not updates:
                continue

            for update in updates:
                user = update.get_user()

                _state = await db.load_state(user.id)
                state = State(_state) if _state else State.NOT_STARTED

                next_state = await fsm.transit(state, update)
                await db.store_state(user.id, next_state.value)

                offset = max(offset, update.update_id) + 1
                await db.store_updates_offset(offset)

            await asyncio.sleep(4)


if __name__ == "__main__":
    asyncio.run(main())
