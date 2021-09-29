import json

import pytest
from pydantic import Field
from pydantic import ValidationError

from consigliere.scheme import base


def test_exclude_unset() -> None:
    class Klass(base.TelegramBotApiType):
        attr1: int = Field(...)
        attr2: int = Field(0)

    assert Klass(attr1=1).dict() == {"attr1": 1}
    assert Klass(attr1=1).json() == '{"attr1": 1}'
    assert Klass(attr1=1, attr2=2).dict() == {"attr1": 1, "attr2": 2}
    assert Klass(attr1=1, attr2=2).json() == '{"attr1": 1, "attr2": 2}'


def test_request() -> None:
    assert base.Request().dict() == {}


def test_response_parameters():
    assert base.ResponseParameters().dict() == {}
    assert base.ResponseParameters(migrate_to_chat_id=1).dict() == {
        "migrate_to_chat_id": 1
    }
    assert base.ResponseParameters(retry_after=1).dict() == {"retry_after": 1}


def test_response():
    assert base.Response(ok=True).dict() == {"ok": True}
    assert base.Response.parse_obj({"ok": 1}) == {"ok": True}
    assert base.Response.parse_obj({"ok": "on"}) == {"ok": True}
    assert base.Response.parse_obj({"ok": "yes"}) == {"ok": True}
    assert base.Response.parse_obj({"ok": "true"}) == {"ok": True}
    assert base.Response.parse_obj({"ok": 0}) == {"ok": False}
    assert base.Response.parse_obj({"ok": "off"}) == {"ok": False}
    assert base.Response.parse_obj({"ok": "no"}) == {"ok": False}
    assert base.Response.parse_obj({"ok": "false"}) == {"ok": False}


def test_str64():
    class Klass(base.TelegramBotApiType):
        attr: base.Str64

    assert Klass(attr="a").dict() == {"attr": "a"}

    with pytest.raises(ValidationError) as err:
        Klass()
    data = json.loads(err.value.json())[0]
    assert data["loc"] == ["attr"]
    assert data["msg"] == "field required"
    assert data["type"] == "value_error.missing"

    with pytest.raises(ValidationError) as err:
        Klass(attr="")
    data = json.loads(err.value.json())[0]
    assert data["loc"] == ["attr"]
    assert data["msg"] == "ensure this value has at least 1 characters"
    assert data["type"] == "value_error.any_str.min_length"

    with pytest.raises(ValidationError) as err:
        Klass(attr="a" * 65)
    data = json.loads(err.value.json())[0]
    assert data["loc"] == ["attr"]
    assert data["msg"] == "ensure this value has at most 64 characters"
    assert data["type"] == "value_error.any_str.max_length"
