# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from typing import Union
import colemen_utils as _c
from marshmallow import Schema, fields, validate, ValidationError
import copper_rabbit.settings as _settings
from copper_rabbit.support.timestamp import current_unix_timestamp

class DeletedTimestamp(fields.Field):
    """Field that serializes an integer and deserializes to a past integer."""

    def _serialize(self, value:Union[int,str], attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value,(int)):
            return value

        return value

    def _deserialize(self, value:int, attr, data, **kwargs):
        if value is None:
            return value
        value = round(value)
        if isinstance(value,(int)) is False:
            raise ValidationError(f"Invalid Deleted timestamp '{value}' [{type(value)}] - expected an integer.")


        if value > current_unix_timestamp():
            raise ValidationError(f"Invalid Deleted timestamp '{value}' Timestamp must be in the past")

        return value
