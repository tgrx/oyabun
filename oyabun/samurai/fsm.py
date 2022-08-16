import abc
import asyncio
from typing import Callable

import attrs

from oyabun.bot import Bot
from oyabun.samurai.states import State
from oyabun.samurai.util import json_dumps
from oyabun.telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton


class Transition(abc.ABC):
    def __init__(self, bot: Bot, update: Update):
        self._bot = bot
        self._update = update

    @abc.abstractmethod
    async def accepts(self, state: State) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def transit(self) -> State:
        raise NotImplementedError


class Start(Transition):
    async def accepts(self, state: State) -> bool:
        if state != State.UNKNOWN:
            return False

        if not self._update.message:
            return False

        if not self._update.message.text:
            return False

        return True

    async def transit(self) -> State:
        me, chat, whi = asyncio.gather(
            self._bot.getMe(),
            self._bot.getChat(chat_id=self._update.message.chat.id),
            self._bot.getWebhookInfo(),
        )

        messages = (
            "Let's begin the test.",
            "I'll send you some debug info about internals.",
            f"*Bot*\n\n```{json_dumps(me)}```",
            f"*Chat*\n\n```{json_dumps(chat)}```",
            f"*Webhook*\n\n```{json_dumps(whi)}```",
            f"Now please send me some plain text:",
        )

        for message in messages:
            await self._bot.sendMessage(
                chat_id=self._update.message.chat.id,
                parse_mode="MarkdownV2",
                text=message,
            )

        return State.S_WAIT_FOR_PLAIN_TEXT


class RespondToPlainText(Transition):
    async def accepts(self, state: State) -> bool:
        if state != State.S_WAIT_FOR_PLAIN_TEXT:
            return False

        if not self._update.message:
            return False

        if not self._update.message.text:
            return False

        return True

    async def transit(self) -> State:
        input_text = self._update.message.text

        messages = (
            (f"Got your message: {input_text!r}.", self._update.message.message_id,),
            ("Now edit some of your text messages, let's see what happens.", None,),
        )

        for message, reply_to in messages:
            await self._bot.sendMessage(
                chat_id=self._update.message.chat.id,
                reply_to_message_id=reply_to,
                text=message,
            )

        return State.S_WAIT_FOR_EDITING_TEXT


class RespondToEditingText(Transition):
    async def accepts(self, state: State) -> bool:
        if state != State.S_WAIT_FOR_EDITING_TEXT:
            return False

        if not self._update.edited_message:
            return False

        if not self._update.edited_message.text:
            return False

        return True

    async def transit(self) -> State:
        edited_text = self._update.edited_message.text

        chat_id = self._update.edited_message.chat.id

        await self._bot.sendMessage(
            chat_id=chat_id,
            reply_to_message_id=self._update.edited_message.message_id,
            text=f"Your new message: {edited_text!r}.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Press to test inline button",
                            callback_data=State.S_SEND_PHOTO.value,
                        ),
                    ],
                ],
            ),
        )

        return State.S_SEND_PHOTO
