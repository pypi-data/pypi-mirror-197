# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


import json
from typing import Union
import zlib
from marshmallow import Schema, fields, validate, ValidationError
import colemen_utils as _c
import copper_rabbit.settings as _settings

class RequestLog(fields.Field):
    """Field that serializes a json string to its log array and deserializes to BINARY compressed json."""

    def _serialize(self, value:Union[int,str], attr, obj, **kwargs):
        if value is None:
            return None
        value = zlib.decompress(value).decode()
        if isinstance(value,(str)) is False:
            return None
        value = json.loads(value)

        return value

    def _deserialize(self, value:Union[list,dict], attr, data, **kwargs):
        if value is None:
            return value
        if isinstance(value,(list,dict)) is False:
            raise ValidationError(f"Invalid Request Log '{value}'")

        value = _c.arr.force_list(value)
        # @Mstep [] convert to a json string
        value = json.dumps(value)
        # @Mstep [] compress the json to a bytes(binary) value.
        value = zlib.compress(value.encode())


        # value = int(value)
        return value
