from functools import wraps
from typing import Any
from typing import Callable
from uuid import uuid4

from aiohttp import web

from oyabun.telegram import Response
from oyabun.telegram import User
from oyabun.telegram.base import TelegramBotApiType

_method_handlers: dict[str, Callable] = {}


def api_method(handler: Callable) -> Callable:
    @wraps(handler)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            obj = await handler(*args, **kwargs)
            rs: Response = Response(
                ok=True,
                result=obj,
            )
        except Exception as err:
            rs = Response(
                description=str(err),
                error_code=-1,
                ok=False,
            )

        return web.json_response(body=rs.jsonb())

    _method_handlers[handler.__name__] = wrapped
    return wrapped


@api_method
async def answerCallbackQuery(request: web.Request) -> bool:
    rq = await request.json()

    cbq_id = rq.get("callback_query_id")
    assert cbq_id

    return bool(cbq_id == "cbq")  # noqa: SIM901


@api_method
async def getMe(request: web.Request) -> TelegramBotApiType:
    rq = await request.json()
    assert rq == {}

    obj = User(
        first_name="FN",
        id=1,
        is_bot=True,
    )

    return obj


class TelegramApp(web.Application):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__token = str(uuid4())

        for method_name, method_handler in _method_handlers.items():
            url = f"/bot{self.__token}/{method_name}"
            self.router.add_post(url, method_handler)

    def get_telegram_bot_api_token(self) -> str:
        return self.__token
