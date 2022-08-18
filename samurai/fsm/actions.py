import abc
import asyncio

from devtools import debug
from PIL import Image

from oyabun.bot import Bot
from oyabun.telegram import InlineKeyboardButton
from oyabun.telegram import InlineKeyboardMarkup
from oyabun.telegram import Update
from samurai.dirs import DIR_REPO
from samurai.dirs import DIR_TMP
from samurai.util import json_dumps


class AbstractAction(abc.ABC):
    def __init__(self, bot: Bot):
        self._bot = bot

    class NoReaction(RuntimeError):
        pass

    class ReactionFailed(RuntimeError):
        pass

    async def react(self, update: Update) -> None:
        await self._ensure_reaction_on(update)
        try:
            await self._react(update)
        except Exception as err:
            raise self.ReactionFailed(err) from err

    @abc.abstractmethod
    async def _ensure_reaction_on(self, update: Update) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _react(self, update: Update) -> None:
        raise NotImplementedError


class Start(AbstractAction):
    async def _ensure_reaction_on(self, update: Update) -> None:
        keywords = {"/start", "restart"}
        if not update.message or update.message.text not in keywords:
            raise self.NoReaction

    async def _react(self, update: Update) -> None:
        assert update.message
        chat_id = update.message.chat.id

        chat, me, whi = await asyncio.gather(
            self._bot.getChat(chat_id=chat_id),
            self._bot.getMe(),
            self._bot.getWebhookInfo(),
        )

        debug(chat)
        debug(me)
        debug(whi)

        replies = (
            "Let's begin the test\\.",
            "I'll send you some debug info about internals\\.",
            f"*Bot*\n\n```{json_dumps(me.dict())}```",
            f"*Chat*\n\n```{json_dumps(chat.dict())}```",
            f"*Webhook*\n\n```{json_dumps(whi.dict())}```",
            "Now please send me some plain text:",
        )

        debug(replies)

        for reply in replies:
            await self._bot.sendMessage(
                chat_id=chat_id,
                parse_mode="MarkdownV2",
                text=reply,
            )


class RespondToPlainText(AbstractAction):
    async def _ensure_reaction_on(self, update: Update) -> None:
        if not update.message or not update.message.text:
            raise self.NoReaction

    async def _react(self, update: Update) -> None:
        message = update.message
        assert message

        replies = (
            (
                f"Got your message: {message.text!r}.",
                message.message_id,
            ),
            (
                "Now edit some of your text messages, let's see what happens.",
                None,
            ),
        )

        for reply, reply_to in replies:
            await self._bot.sendMessage(
                chat_id=message.chat.id,
                reply_to_message_id=reply_to,
                text=reply,
            )


class RespondToEditingText(AbstractAction):
    async def _ensure_reaction_on(self, update: Update) -> None:
        if not update.edited_message or not update.edited_message.text:
            raise self.NoReaction

    async def _react(self, update: Update) -> None:
        message = update.edited_message
        assert message

        await self._bot.sendMessage(
            chat_id=message.chat.id,
            reply_to_message_id=message.message_id,
            text=f"Your new message: {message.text!r}.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            callback_data="lenna.png",
                            text="Press to test inline button",
                        ),
                    ],
                ],
            ),
        )


class SendPhoto(AbstractAction):
    async def _ensure_reaction_on(self, update: Update) -> None:
        if (
            not update.callback_query
            or not update.callback_query.message  # noqa: W503
            or not update.callback_query.data  # noqa: W503
        ):
            raise self.NoReaction

    async def _react(self, update: Update) -> None:
        assert update.callback_query and update.callback_query.data

        photo = (DIR_REPO / update.callback_query.data).resolve()
        assert photo.is_file(), f"no file: {photo.as_posix()}"

        message = update.callback_query.message
        assert message

        await self._bot.editMessageReplyMarkup(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [],
                ],
            ),
        )

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


class ReplyWithProcessedPhoto(AbstractAction):
    async def _ensure_reaction_on(self, update: Update) -> None:
        if not update.message or not update.message.photo:
            raise self.NoReaction

    async def _react(self, update: Update) -> None:
        message = update.message
        assert message and message.photo

        photo_size_obj = max(
            message.photo,
            key=lambda _i: (_i.file_size, _i.width * _i.height),
        )

        file_obj = await self._bot.getFile(file_id=photo_size_obj.file_id)
        assert file_obj.file_path, f"no file_path in: {file_obj}"

        buffer = await self._bot.downloadFile(file=file_obj)
        image = Image.open(buffer).convert(mode="L").convert(mode="RGB")

        file_name = f"{file_obj.file_unique_id}{file_obj.file_path[-4:]}"
        file_path = (DIR_TMP / file_name).resolve()
        with file_path.open("wb") as stream:
            image.save(stream)

        sent = await self._bot.sendPhoto(
            chat_id=message.chat.id,
            photo=file_path,
        )

        await self._bot.editMessageCaption(
            caption="Noir",
            chat_id=sent.chat.id,
            message_id=sent.message_id,
        )

        await self._bot.sendMessage(
            chat_id=message.chat.id,
            text="All tests are passed successfully.",
        )


class Restart(AbstractAction):
    async def _ensure_reaction_on(self, update: Update) -> None:
        assert update

    async def _react(self, update: Update) -> None:
        message = update.message
        assert message

        text = "If you want to restart the test, just type 'restart'."

        sent = await self._bot.sendMessage(
            chat_id=message.chat.id,
            text=text,
        )

        await self._bot.editMessageText(
            chat_id=sent.chat.id,
            message_id=sent.message_id,
            text=f"{text}.\n\nUPD: or use: /start",
        )
