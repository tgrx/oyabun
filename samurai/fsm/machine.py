import traceback
from typing import Any
from typing import Type
from typing import TypeVar

from oyabun.bot import Bot
from oyabun.telegram import Update
from samurai.fsm.actions import AbstractAction
from samurai.persistence import Persistence

StateT = TypeVar("StateT")


class FSM:
    def __init__(self, db: Persistence, bot: Bot):
        self._bot = bot
        self._db: Persistence = db
        self._stt: dict[tuple[Any, Any], AbstractAction] = {}

    def register(
        self,
        state0: StateT,
        state1: StateT,
        action_cls: Type[AbstractAction],
    ) -> "FSM":
        key = (state0, state1)
        if key not in self._stt:
            action = action_cls(self._bot)
            self._stt[key] = action
        return self

    async def transit(self, state: StateT, update: Update) -> StateT:
        chat = update.get_chat()

        next_state = state

        for (state0, state1), action in self._stt.items():
            if state0 != state:
                continue

            try:
                await action.react(update)
            except AbstractAction.NoReaction:
                continue
            except AbstractAction.ReactionFailed as err:
                traceback.print_exc()

                await self._bot.sendMessage(
                    chat_id=chat.id,
                    text=f"ERROR: {err}",
                )
                continue

            next_state = state1

        return next_state
