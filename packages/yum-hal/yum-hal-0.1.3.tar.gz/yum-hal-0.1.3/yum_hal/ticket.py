import msgpack
import base64
import json

from typing import Dict, Union, Sequence, Mapping
from uuid import uuid4
from datetime import datetime

from .errors import YumError

wtype = Union[int, float, bool, None, Sequence, Mapping, datetime]

_DTFORMAT = "%Y%m%d%H%M%S%f"


def decode_datetime(obj):
    if "_dt_" in obj:
        obj = datetime.strptime(obj["as_str"], _DTFORMAT)
    return obj


def encode_datetime(obj):
    if isinstance(obj, datetime):
        return {"_dt_": True, "as_str": obj.strftime(_DTFORMAT)}
    return obj


def _encode(obj) -> str:
    kvs = {}
    if isinstance(obj, Ticket):
        kvs["id"] = obj.id
        kvs["code"] = obj.code
        kvs["birth_time"] = obj.birth_time
        kvs["body"] = (obj.body,)
        kvs["status"] = obj.status

    if isinstance(obj, Feedback):
        kvs["for_id"] = obj.for_id

    bs = msgpack.packb(kvs, default=encode_datetime)
    if isinstance(bs, bytes):
        return base64.urlsafe_b64encode(bs).decode()

    raise YumError(reason="encode error")


def _decode(obj, msg: str) -> None:
    bs = base64.urlsafe_b64decode(msg)
    t = msgpack.unpackb(bs, object_hook=decode_datetime)

    if isinstance(obj, Ticket):
        obj.id = t.get("id")
        obj.code = t.get("code")
        obj.birth_time = t.get("birth_time")
        b = t.get("body")
        if isinstance(b, list):
            obj.body = b[0]
        elif isinstance(b, dict):
            obj.body = b
        obj.status = t.get("status")

    if isinstance(obj, Feedback):
        obj.for_id = t.get("for_id")


class Ticket(object):
    def __init__(self, code: str, status: int = 200) -> None:
        super(Ticket, self).__init__()
        self.id = str(uuid4()).replace("-", "")
        self.birth_time = datetime.now()
        self.code = code
        self.status = status
        self.body = {}

    def __repr__(self) -> str:
        j = self.__dict__.copy()
        j["body"] = self.body.copy()
        j["birth_time"] = self.birth_time.strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(j, ensure_ascii=False)

    def put(self, name: str, value: wtype) -> None:
        self.body[name] = value

    def put_all(self, values: Dict) -> None:
        self.body.update(values)

    def take(self, name: str, default_value: wtype = None) -> wtype:
        return self.body.get(name, default_value)

    def encode(self) -> str:
        return _encode(self)

    def decode(self, msg: str) -> None:
        _decode(self, msg)


class Feedback(Ticket):
    def __init__(self, ticket: Ticket, status: int = 200) -> None:
        super(Feedback, self).__init__(ticket.code, status)
        self.for_id = ticket.id
