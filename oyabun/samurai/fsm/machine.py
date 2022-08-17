from typing import Type

from oyabun.bot import Bot
from oyabun.samurai.fsm.actions import AbstractAction
from oyabun.samurai.persistence import Persistence
from oyabun.samurai.states import State
from oyabun.samurai.util import json_dumps
from oyabun.telegram import Update, Chat, User


class FSM:
    def __init__(self, db: Persistence, bot: Bot):
        self._bot = bot
        self._db: Persistence = db
        self._actions: dict[Type[AbstractAction], AbstractAction] = {}

    def register(self, state: State, action_cls: Type[AbstractAction]) -> None:
        if action_cls in self._actions:
            return

        action = action_cls(state, self._bot)

    async def transit(self, update: Update) -> None:
        chat: Chat
        user: User

        if update.message:
            chat = update.message.chat
            user = update.message.from_
        elif update.edited_message:
            chat = update.edited_message.chat
            user = update.edited_message.from_
        elif update.callback_query and update.callback_query.message:
            chat = update.callback_query.message.chat
            user = update.callback_query.message.from_
        else:
            err = f"cannot get user and chat from:\n{json_dumps(update)}\n"
            raise RuntimeError(err)

        current = await self._db.load_state(user.id)
        transition_cls = self._matrix.get(current)
        if not transition_cls:
            await self._bot.sendMessage(
                chat_id=chat.id,
                text=f"ERROR: unknown state {current!r}",
            )
            return

        transition = transition_cls(bot=self._bot, update=update)
        if not await transition.accepts(current):
            await self._bot.sendMessage(
                chat_id=chat.id,
                text=f"Sorry I will ignore that.",
            )
            return

        new = await transition.transit()

        await self._db.store_state(user.id, new)
