from datetime import UTC
from datetime import datetime
from oyabun.telegram import base


def test_exclude_unset() -> None:
    class Klass(base.TelegramBotApiType):
        attr1: int
        attr2: int = 0

    k1 = Klass(attr1=1)
    assert k1.model_dump() == {"attr1": 1}
    assert k1.model_dump_json() == '{"attr1":1}'
    assert k1.model_dump_jsonb() == b'{"attr1":1}'

    k2 = Klass(attr1=1, attr2=2)
    assert k2.model_dump() == {"attr1": 1, "attr2": 2}
    assert k2.model_dump_json() == '{"attr1":1,"attr2":2}'
    assert k2.model_dump_jsonb() == b'{"attr1":1,"attr2":2}'


def test_orjson_dumps() -> None:
    class Klass(base.TelegramBotApiType):
        attr: datetime

    ts = datetime(
        year=2022,
        month=8,
        day=12,
        hour=2,
        minute=45,
        second=10,
        tzinfo=UTC,
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

    assert obj1.model_dump() == {"attr": ts}
    assert obj1.model_dump_json() == '{"attr":"2022-08-12T02:45:10Z"}'
    assert obj1.model_dump_jsonb() == b'{"attr":"2022-08-12T02:45:10Z"}'

    assert obj2.model_dump() == {"attr": ts.replace(tzinfo=None)}
    assert obj2.model_dump_json() == '{"attr":"2022-08-12T02:45:10"}'
    assert obj2.model_dump_jsonb() == b'{"attr":"2022-08-12T02:45:10"}'

    assert obj3.model_dump() == {"attr": ts}
    assert obj3.model_dump_json() == '{"attr":"2022-08-12T02:45:10Z"}'
    assert obj3.model_dump_jsonb() == b'{"attr":"2022-08-12T02:45:10Z"}'

    assert obj4.model_dump() == {"attr": ts}
    assert obj4.model_dump_json() == '{"attr":"2022-08-12T02:45:10Z"}'
    assert obj4.model_dump_jsonb() == b'{"attr":"2022-08-12T02:45:10Z"}'

    assert obj5.model_dump() == {"attr": ts}
    assert obj5.model_dump_json() == '{"attr":"2022-08-12T02:45:10Z"}'
    assert obj5.model_dump_jsonb() == b'{"attr":"2022-08-12T02:45:10Z"}'


def test_request() -> None:
    assert base.Request().model_dump() == {}


def test_response_parameters() -> None:
    assert base.ResponseParameters().model_dump() == {}
    assert base.ResponseParameters(
        migrate_to_chat_id=1,
    ).model_dump() == {"migrate_to_chat_id": 1}
    assert base.ResponseParameters(retry_after=1).model_dump() == {
        "retry_after": 1
    }


def test_response() -> None:
    assert base.Response(ok=True).model_dump() == {"ok": True}
    assert base.Response.model_validate({"ok": 1}).model_dump() == {"ok": True}
    assert base.Response.model_validate({"ok": "on"}).model_dump() == {
        "ok": True
    }
    assert base.Response.model_validate({"ok": "yes"}).model_dump() == {
        "ok": True
    }
    assert base.Response.model_validate({"ok": "true"}).model_dump() == {
        "ok": True
    }
    assert base.Response.model_validate({"ok": 0}).model_dump() == {
        "ok": False
    }
    assert base.Response.model_validate({"ok": "off"}).model_dump() == {
        "ok": False
    }
    assert base.Response.model_validate({"ok": "no"}).model_dump() == {
        "ok": False
    }
    assert base.Response.model_validate({"ok": "false"}).model_dump() == {
        "ok": False
    }
