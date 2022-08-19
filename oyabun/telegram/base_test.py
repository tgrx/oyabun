from datetime import datetime
from datetime import timezone

from pydantic import Field

from oyabun.telegram import base


def test_exclude_unset() -> None:
    class Klass(base.TelegramBotApiType):
        attr1: int = Field(...)
        attr2: int = Field(0)

    k1 = Klass(attr1=1)
    assert k1.dict() == {"attr1": 1}
    assert k1.json() == '{"attr1":1}'
    assert k1.jsonb() == b'{"attr1":1}'

    k2 = Klass(attr1=1, attr2=2)
    assert k2.dict() == {"attr1": 1, "attr2": 2}
    assert k2.json() == '{"attr1":1,"attr2":2}'
    assert k2.jsonb() == b'{"attr1":1,"attr2":2}'


def test_orjson_dumps() -> None:
    class Klass(base.TelegramBotApiType):
        attr: datetime = Field(...)

    ts = datetime(
        year=2022,
        month=8,
        day=12,
        hour=2,
        minute=45,
        second=10,
        tzinfo=timezone.utc,
    )

    obj1 = Klass(attr=ts)
    obj2 = Klass(attr=ts.strftime("%Y-%m-%dT%H:%M:%S"))  # type: ignore
    obj3 = Klass(attr=ts.strftime("%Y-%m-%dT%H:%M:%S+00:00"))  # type: ignore
    obj4 = Klass(attr=ts.isoformat())  # type: ignore
    obj5 = Klass(attr=ts.timestamp())  # type: ignore

    for i, obj in enumerate((obj1, obj2, obj3, obj4, obj5), start=1):
        err = f"field mismatch for obj{i}"
        assert isinstance(obj.attr, datetime), err
        assert obj.attr.year == ts.year, err
        assert obj.attr.month == ts.month, err
        assert obj.attr.day == ts.day, err
        assert obj.attr.hour == ts.hour, err
        assert obj.attr.minute == ts.minute, err
        assert obj.attr.second == ts.second, err

    assert obj1.dict() == {"attr": ts}
    assert obj1.json() == '{"attr":"2022-08-12T02:45:10+00:00"}'
    assert obj1.jsonb() == b'{"attr":"2022-08-12T02:45:10+00:00"}'

    assert obj2.dict() == {"attr": ts.replace(tzinfo=None)}
    assert obj2.json() == '{"attr":"2022-08-12T02:45:10"}'
    assert obj2.jsonb() == b'{"attr":"2022-08-12T02:45:10"}'

    assert obj3.dict() == {"attr": ts}
    assert obj3.json() == '{"attr":"2022-08-12T02:45:10+00:00"}'
    assert obj3.jsonb() == b'{"attr":"2022-08-12T02:45:10+00:00"}'

    assert obj4.dict() == {"attr": ts}
    assert obj4.json() == '{"attr":"2022-08-12T02:45:10+00:00"}'
    assert obj4.jsonb() == b'{"attr":"2022-08-12T02:45:10+00:00"}'

    assert obj5.dict() == {"attr": ts}
    assert obj5.json() == '{"attr":"2022-08-12T02:45:10+00:00"}'
    assert obj5.jsonb() == b'{"attr":"2022-08-12T02:45:10+00:00"}'


def test_request() -> None:
    assert base.Request().dict() == {}


def test_response_parameters() -> None:
    assert base.ResponseParameters().dict() == {}
    assert base.ResponseParameters(migrate_to_chat_id=1).dict() == {
        "migrate_to_chat_id": 1
    }
    assert base.ResponseParameters(retry_after=1).dict() == {"retry_after": 1}


def test_response() -> None:
    assert base.Response(ok=True).dict() == {"ok": True}
    assert base.Response.parse_obj({"ok": 1}) == {"ok": True}
    assert base.Response.parse_obj({"ok": "on"}) == {"ok": True}
    assert base.Response.parse_obj({"ok": "yes"}) == {"ok": True}
    assert base.Response.parse_obj({"ok": "true"}) == {"ok": True}
    assert base.Response.parse_obj({"ok": 0}) == {"ok": False}
    assert base.Response.parse_obj({"ok": "off"}) == {"ok": False}
    assert base.Response.parse_obj({"ok": "no"}) == {"ok": False}
    assert base.Response.parse_obj({"ok": "false"}) == {"ok": False}
