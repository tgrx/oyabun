import asyncio
import os
from pathlib import Path

import aiosqlite
from devtools import debug
from dotenv import load_dotenv

from oyabun.bot import Bot

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN") or ""
assert token, "cannot start: TELEGRAM_BOT_TOKEN is not set"

db_file = Path(__file__).parent.parent.resolve() / ".artifacts" / "samurai.db"
db_file = db_file.resolve()


async def main() -> None:
    bot = Bot(token)

    async with aiosqlite.connect(db_file.as_posix()) as db:
        await init_db(db)

        while True:
            print("\n", "-" * 30, "cycle", "-" * 30)  # noqa: T201

            offset = await get_updates_offset(db)
            debug(offset)

            updates = await bot.getUpdates(offset=offset, timeout=10)
            if not updates:
                continue

            for update in updates:
                offset = max(offset, update.update_id)

                debug(update)

            await save_updates_offset(db, offset)

            print("z-z-z...")  # noqa: T201
            await asyncio.sleep(10)


async def init_db(db: aiosqlite.Connection) -> None:
    db.row_factory = aiosqlite.Row

    await db.execute(
        """
        create table if not exists
        samurai_metadata(
            id integer not null primary key,
            value_i integer
        );
        """
    )
    await db.commit()

    await db.execute(
        """
        replace into samurai_metadata(id, value_i)
        values(:id, :value_i);
        """,
        {
            "id": 1,
            "value_i": 0,
        },
    )
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
