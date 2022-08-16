import asyncio
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from typing import Union

import orjson

from oyabun.samurai.dirs import DIR_ARTIFACTS
from oyabun.samurai.states import State


class Persistence:
    DB_FILE = DIR_ARTIFACTS / "samurai.json"

    async def load_state(self, user_id: Union[str, int]) -> State:
        db = await self._load_db()
        value = db.get("user_states", {}).get(user_id) or State.UNKNOWN.value
        return State(value)

    async def store_state(self, user_id: Union[str, int], state: State) -> None:
        db = await self._load_db()
        db.setdefault("user_states", {})[user_id] = state.value
        await self._store_db(db)

    async def load_updates_offset(self) -> int:
        db = await self._load_db()
        value = db.get("updates_offset") or 0
        return int(value)

    async def store_updates_offset(self, updates_offset: int) -> None:
        db = await self._load_db()
        db["updates_offset"] = updates_offset
        await self._store_db(db)

    def __init__(self):
        self.__executor = ThreadPoolExecutor(
            max_workers=cpu_count() * 2 + 1,
            thread_name_prefix=self.__class__.__name__,
        )

    async def _load_db(self) -> dict:
        def _do():
            if not self.DB_FILE.is_file():
                return {}

            with self.DB_FILE.open("r") as stream:
                try:
                    return orjson.loads(stream.read())
                except orjson.JSONDecodeError:
                    return {}

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.__executor, _do)

    async def _store_db(self, db: dict) -> None:
        def _sync():
            options = orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS | orjson.OPT_APPEND_NEWLINE
            with self.DB_FILE.open("wb") as stream:
                stream.write(orjson.dumps(db, option=options))

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.__executor, _sync)
