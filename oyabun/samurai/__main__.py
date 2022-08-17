import asyncio
import os

from devtools import debug
from dotenv import load_dotenv

from oyabun.bot import Bot
from oyabun.samurai.fsm import actions
from oyabun.samurai.fsm.machine import FSM
from oyabun.samurai.persistence import Persistence
from oyabun.samurai.states import State
from oyabun.telegram import User

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN") or ""
assert token, "cannot start: TELEGRAM_BOT_TOKEN is not set"


async def main() -> None:  # noqa:CCR001
    bot = Bot(token)
    db = Persistence()
    fsm = FSM(db, bot)

    fsm.register(  # noqa: ECE001
        State.NOT_STARTED,
        State.WAIT_FOR_PLAIN_TEXT,
        actions.Start,
    ).register(
        State.WAIT_FOR_PLAIN_TEXT,
        State.WAIT_FOR_EDITING_TEXT,
        actions.RespondToPlainText,
    ).register(
        State.WAIT_FOR_EDITING_TEXT,
        State.SEND_PHOTO,
        actions.RespondToEditingText,
    ).register(
        State.SEND_PHOTO,
        State.WAIT_FOR_PHOTO,
        actions.SendPhoto,
    ).register(
        State.WAIT_FOR_PHOTO,
        State.FINISHED,
        actions.ReplyWithProcessedPhoto,
    ).register(
        State.FINISHED,
        State.NOT_STARTED,
        actions.Restart,
    )

    while True:
        print("\n", "-" * 30, "cycle", "-" * 30)  # noqa: T201

        offset = await db.load_updates_offset()
        debug(offset)

        updates = await bot.getUpdates(offset=offset, timeout=30)
        if not updates:
            continue

        for update in updates:
            user: User
            if update.message and update.message.from_:
                user = update.message.from_
            elif update.edited_message and update.edited_message.from_:
                user = update.edited_message.from_
            elif update.callback_query:
                user = update.callback_query.from_
            else:
                raise RuntimeError(f"cannot get user from {update}")

            state_value: str = await db.load_state(user.id)
            state = State(state_value) if state_value else State.NOT_STARTED

            next_state = await fsm.transit(state, update)
            await db.store_state(user.id, next_state.value)

            offset = max(offset, update.update_id) + 1
            await db.store_updates_offset(offset)

        await asyncio.sleep(4)


if __name__ == "__main__":
    asyncio.run(main())
