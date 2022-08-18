from typing import Any

import orjson


def json_dumps(obj: Any) -> str:
    options = (
        orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS | orjson.OPT_APPEND_NEWLINE
    )
    return orjson.dumps(obj, option=options).decode()
