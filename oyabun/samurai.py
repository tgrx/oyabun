import asyncio
import enum
import os
from contextlib import suppress
from functools import partial
from pathlib import Path
from typing import Any
from typing import Callable

import aiosqlite
import orjson
import platformdirs
from devtools import debug
from dotenv import load_dotenv
from PIL import Image

from oyabun.bot import Bot
from oyabun.telegram import InlineKeyboardButton
from oyabun.telegram import InlineKeyboardMarkup
from oyabun.telegram import Update
from oyabun.telegram import User

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN") or ""
assert token, "cannot start: TELEGRAM_BOT_TOKEN is not set"

db_file = Path(__file__).parent.parent.resolve() / ".artifacts" / "samurai.db"
db_file = db_file.resolve()


async def main() -> None:
    bot = Bot(token)

    async with aiosqlite.connect(db_file.as_posix()) as db:
        await init_db(db)

        process = partial(process_update, bot, db)

        while True:
            print("\n", "-" * 30, "cycle", "-" * 30)  # noqa: T201

            offset = await get_updates_offset(db)
            debug(offset)

            updates = await bot.getUpdates(offset=offset, timeout=10)
            if not updates:
                continue

            for update in updates:
                offset = max(offset, update.update_id)

                await process(update)

            await save_updates_offset(db, offset)

            print("z-z-z...")  # noqa: T201
            await asyncio.sleep(10)


@enum.unique
class State(enum.Enum):
    UNKNOWN = ""
    S_01_TEXT = "01-text"
    S_02_EDIT_TEXT = "02-edit-text"
    S_03_PHOTO_FROM_BOT = "03-photo-from-bot"
    S_04_PHOTO_TO_BOT = "04-photo-to-bot"
    FINISHED = "99-finished"


async def process_update(  # noqa: CCR001
    bot: Bot,
    db: aiosqlite.Connection,
    update: Update,
) -> None:
    if update.message:
        chat = update.message.chat
        user = update.message.from_
    elif update.edited_message:
        chat = update.edited_message.chat
        user = update.edited_message.from_
    elif update.callback_query and update.callback_query.message:
        chat = update.callback_query.message.chat
        user = update.callback_query.from_
    else:
        raise RuntimeError(f"no user in update {update}")

    assert chat
    assert user
    state = await get_state(db, user)

    if state == State.UNKNOWN:
        await bot.sendMessage(
            chat_id=chat.id,
            text="Начинаем тест. Сейчас я покажу тебе всякую информацию.",
        )

        jd_ = partial(
            orjson.dumps,
            option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS,
        )
        jd: Callable[[Any], str] = lambda *args, **kwargs: jd_(
            *args, **kwargs
        ).decode()

        me = await bot.getMe()
        wh = await bot.getWebhookInfo()
        chat = await bot.getChat(chat_id=chat.id)
        await bot.sendMessage(
            chat_id=chat.id,
            text=(
                f"""
*Инфа*

_Бот_

```json
{jd(me.dict())}
```

_Вебхук_

```json
{jd(wh.dict())}
```

_Чат_

```json
{jd(chat.dict())}
```

_Юзер_

```json
{jd(user.dict())}
```
                """
            ),
            parse_mode="MarkdownV2",
        )

        await bot.sendMessage(
            chat_id=chat.id,
            text="Теперь отправь какой-нибудь текст",
        )
        await set_state(db, user, State.S_01_TEXT)
        return

    if state == State.S_01_TEXT:
        if not update.message or not update.message.text:
            await bot.sendMessage(
                chat_id=chat.id,
                text="Отказываюсь. Ещё раз.",
            )
            return

        await bot.sendMessage(
            chat_id=chat.id,
            text=(
                f"Твой текст: {update.message.text!r}. "
                f"Теперь отредактируй это сообщение, только текст поменяй."
            ),
            reply_to_message_id=update.message.message_id,
        )
        await set_state(db, user, State.S_02_EDIT_TEXT)
        return

    if state == State.S_02_EDIT_TEXT:
        if not update.edited_message or not update.edited_message.text:
            await bot.sendMessage(
                chat_id=chat.id,
                text="Отказываюсь. Ещё раз.",
            )
            return

        await bot.sendMessage(
            chat_id=update.edited_message.chat.id,
            text=(
                f"Твой отредактированный текст: "
                f"{update.edited_message.text!r}."
            ),
            reply_to_message_id=update.edited_message.message_id,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Фото",
                            callback_data=State.S_03_PHOTO_FROM_BOT.value,
                        ),
                    ],
                ],
            ),
        )
        await set_state(db, user, State.S_03_PHOTO_FROM_BOT)
        return

    if state == State.S_03_PHOTO_FROM_BOT:
        if not update.callback_query:
            await bot.sendMessage(
                chat_id=chat.id,
                text="Игнорирую. Кнопку жми!",
            )
            return

        with suppress(bot.RequestError):
            await bot.answerCallbackQuery(
                callback_query_id=update.callback_query.id,
                text="кнопка ок!",
            )

        home = Path(platformdirs.user_documents_dir()).parent.resolve()
        desktop = (home / "Desktop").resolve()
        ph = desktop / "clearsee_timeouts.png"

        await bot.sendPhoto(
            caption="Теперь жду фото от тебя.",
            chat_id=chat.id,
            photo=ph,
        )
        await set_state(db, user, State.S_04_PHOTO_TO_BOT)
        return

    if state == State.S_04_PHOTO_TO_BOT:
        if not update.message or not update.message.photo:
            await bot.sendMessage(
                chat_id=chat.id,
                text="Игнорирую. Фотку давай!",
            )
            return

        tmp = Path(__file__).parent.parent / "tmp"

        photo_size_obj = max(
            update.message.photo,
            key=lambda _i: (_i.file_size, _i.width * _i.height),
        )
        file_obj = await bot.getFile(file_id=photo_size_obj.file_id)
        buffer = await bot.downloadFile(file=file_obj)

        image = Image.open(buffer).convert(mode="L").convert(mode="RGB")

        assert file_obj.file_path
        file_path = tmp / f"{file_obj.file_unique_id}{file_obj.file_path[-4:]}"
        file_path = file_path.resolve()
        with file_path.open("wb") as stream:
            image.save(stream)

        await bot.sendPhoto(
            chat_id=update.message.chat.id,
            photo=file_path,
            caption="тест пройден",
        )

        await set_state(db, user, State.UNKNOWN)
        return

    await bot.sendMessage(
        chat_id=chat.id,
        text=(
            "Тест пройден! Хочешь начать заново? "
            "Отправь что-нибудь и тест перезапустится."
        ),
    )
    await set_state(db, user, State.UNKNOWN)
    return


async def get_state(db: aiosqlite.Connection, user: User) -> State:
    sql = """
    select state from samurai_state where user_id = :user_id limit 1;
    """

    params = {
        "user_id": user.id,
    }

    async with db.execute(sql, params) as cursor:
        row = await cursor.fetchone()
        if not row:
            return State.UNKNOWN

        try:
            state = State(row["state"])
        except ValueError:
            state = State.UNKNOWN

    return state


async def set_state(
    db: aiosqlite.Connection, user: User, state: State
) -> None:
    sql = """
    REPLACE INTO samurai_state(user_id, state)
    VALUES
    (:user_id, :state)
    ;
    """

    params = {
        "user_id": user.id,
        "state": state.value,
    }

    async with db.execute(sql, params):
        await db.commit()


async def init_db(db: aiosqlite.Connection) -> None:
    db.row_factory = aiosqlite.Row

    sql_create_metadata = """
    CREATE TABLE IF NOT EXISTS
    samurai_metadata(
        id INTEGER NOT NULL PRIMARY KEY,
        value_i INTEGER
    )
    ;
    """

    sql_create_state = """
    CREATE TABLE IF NOT EXISTS
    samurai_state(
        id INTEGER NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL UNIQUE,
        state text
    )
    ;
    """

    sql_init_metadata = """
    REPLACE INTO samurai_metadata(id, value_i)
    VALUES
    (:id, :value_i)
    ;
    """

    queries: tuple[tuple[str, dict[str, Any]], ...] = (
        (sql_create_metadata, {}),
        (sql_create_state, {}),
        (
            sql_init_metadata,
            {
                "id": 1,
                "value_i": 0,
            },
        ),
    )

    for sql, params in queries:
        async with db.execute(sql, params):
            await db.commit()


async def get_updates_offset(db: aiosqlite.Connection) -> int:
    sql = "select value_i from samurai_metadata where id = :id;"

    cursor: aiosqlite.Cursor
    async with db.execute(sql, {"id": 1}) as cursor:
        row = await cursor.fetchone()
        offset = 0 if row is None else row["value_i"]

    assert isinstance(offset, int)

    return offset


async def save_updates_offset(db: aiosqlite.Connection, offset: int) -> None:
    offset += 1

    async with db.execute(
        """
        update samurai_metadata
        set value_i = :value_i
        where id = :id
        """,
        {
            "id": 1,
            "value_i": offset,
        },
    ):
        pass


if __name__ == "__main__":
    asyncio.run(main())
