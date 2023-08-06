# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from typing import Union
import colemen_utils as _c
from marshmallow import Schema, fields, validate, ValidationError
import copper_rabbit.settings as _settings

class RequestMethod(fields.Field):
    """Field that serializes a request method name using aliases."""

    def _serialize(self, value:Union[int,str], attr, obj, **kwargs):
        # print(f"RequestMethod._serialize.attr:{attr}")
        # print(f"RequestMethod._serialize.obj:{obj}")
        # print(f"RequestMethod._serialize.kwargs:{kwargs}")
        if value is None:
            return None

        if value not in _settings.datas.valid_request_methods:
            return None

        return value

    def _deserialize(self, value:Union[int,str], attr, data, **kwargs):
        # print(f"RequestMethod._deserialize.attr:{attr}")
        # print(f"RequestMethod._deserialize.data:{data}")
        # print(f"RequestMethod._deserialize.kwargs:{kwargs}")
        if value is None:
            return value

        valid_value = _c.valid.request_method(value)

        if valid_value is False:
            raise ValidationError(f"Invalid Method type '{value}' - expected: [{', '.join(_settings.datas.valid_request_methods)}]")

        return value
