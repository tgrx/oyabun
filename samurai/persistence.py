import asyncio
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

import orjson

from samurai.dirs import DIR_ARTIFACTS


class Persistence:
    DB_FILE = DIR_ARTIFACTS / "samurai.json"

    async def load_state(self, user_id: str | int) -> str:
        db = await self._load_db()
        state: str = db.get("user_states", {}).get(str(user_id))
        return state

    async def store_state(self, user_id: str | int, state: str) -> None:
        db = await self._load_db()
        db.setdefault("user_states", {})[str(user_id)] = state
        await self._store_db(db)

    async def load_updates_offset(self) -> int:
        db = await self._load_db()
        value = db.get("updates_offset") or 0
        return int(value)

    async def store_updates_offset(self, updates_offset: int) -> None:
        db = await self._load_db()
        db["updates_offset"] = updates_offset
        await self._store_db(db)

    def __init__(self) -> None:
        nr_cpus = cpu_count()
        assert nr_cpus

        self.__executor = ThreadPoolExecutor(
            max_workers=nr_cpus * 2 + 1,
            thread_name_prefix=self.__class__.__name__,
        )

    async def _load_db(self) -> dict:
        def _do() -> dict:
            if not self.DB_FILE.is_file():
                return {}

            with self.DB_FILE.open("r") as stream:
                try:
                    db = orjson.loads(stream.read())
                    assert isinstance(db, dict)
                    return db
                except orjson.JSONDecodeError:
                    return {}

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.__executor, _do)

    async def _store_db(self, db: dict) -> None:
        def _sync() -> None:
            options = (
                orjson.OPT_INDENT_2
                | orjson.OPT_SORT_KEYS  # noqa: W503
                | orjson.OPT_APPEND_NEWLINE  # noqa: W503
            )
            with self.DB_FILE.open("wb") as stream:
                stream.write(orjson.dumps(db, option=options))

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.__executor, _sync)
