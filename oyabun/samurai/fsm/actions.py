import abc
import asyncio
from typing import TypeVar

from PIL import Image

from oyabun.bot import Bot
from oyabun.samurai.dirs import DIR_REPO, DIR_TMP
from oyabun.samurai.states import State
from oyabun.samurai.util import json_dumps
from oyabun.telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton


StateT = TypeVar("StateT")


class AbstractAction(abc.ABC):
    def __init__(self, state: StateT, bot: Bot):
        self._bot = bot
        self._state = state

    @abc.abstractmethod
    async def accepts(self, state: StateT, update: Update) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def transit(self, state: StateT, update: Update) -> State:
        raise NotImplementedError


class Start(AbstractAction):
    async def accepts(self, state: State) -> bool:
        if state != State.UNKNOWN:
            return False

        if not self._update.message:
            return False

        if self._update.message.text not in {"/start", "restart"}:
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


class RespondToPlainText(AbstractAction):
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


class RespondToEditingText(AbstractAction):
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


class SendPhoto(AbstractAction):
    async def accepts(self, state: State) -> bool:
        if state != State.S_SEND_PHOTO:
            return False

        if not self._update.callback_query:
            return False

        return True

    async def transit(self) -> State:
        photo = DIR_REPO / "lenna.png"

        message = self._update.callback_query.message

        await self._bot.sendPhoto(
            caption="Lena Forsén",
            chat_id=message.chat.id,
            photo=photo,
            reply_to_message_id=message.message_id,
        )

        await self._bot.sendMessage(
            chat_id=message.chat.id,
            text="Now please send me some of your picture:",
        )

        return State.S_WAIT_FOR_PHOTO


class ReplyWithProcessedPhoto(AbstractAction):
    async def accepts(self, state: State) -> bool:
        if state != State.S_WAIT_FOR_PHOTO:
            return False

        if not self._update.message:
            return False

        if not self._update.message.photo:
            return False

        return True

    async def transit(self) -> State:
        message = self._update.message

        photo_size_obj = max(
            message.photo,
            key=lambda _i: (_i.file_size, _i.width * _i.height),
        )

        file_obj = await self._bot.getFile(file_id=photo_size_obj.file_id)
        assert file_obj.file_path

        buffer = await self._bot.downloadFile(file=file_obj)
        image = Image.open(buffer).convert(mode="L").convert(mode="RGB")

        file_name = f"{file_obj.file_unique_id}{file_obj.file_path[-4:]}"
        file_path = (DIR_TMP / file_name).resolve()
        with file_path.open("wb") as stream:
            image.save(stream)

        await self._bot.sendPhoto(
            caption="B & W",
            chat_id=message.chat.id,
            photo=file_path,
        )

        await self._bot.sendMessage(
            chat_id=message.chat.id,
            text="All tests are passed successfully.",
        )

        return State.FINISHED


class Restart(AbstractAction):
    async def accepts(self, state: State) -> bool:
        if state != State.FINISHED:
            return False

        return True

    async def transit(self) -> State:
        message = self._update.message

        await self._bot.sendMessage(
            chat_id=message.chat.id,
            text="If you want to restart the test, just type 'restart'.",
        )

        return State.UNKNOWN
