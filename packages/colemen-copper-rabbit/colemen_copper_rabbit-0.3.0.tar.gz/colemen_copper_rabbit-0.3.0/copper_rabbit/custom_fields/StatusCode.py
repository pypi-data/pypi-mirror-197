# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from typing import Union
from marshmallow import Schema, fields, validate, ValidationError
import copper_rabbit.settings as _settings

class StatusCode(fields.Field):
    """Field that serializes to an string status code and deserializes to an integer."""

    def _serialize(self, value:Union[int,str], attr, obj, **kwargs):
        if value is None:
            return None

        if isinstance(value,(int)):
            value = str(value)

        if value not in _settings.datas.valid_status_codes:
            return None

        return value

    def _deserialize(self, value:Union[int,str], attr, data, **kwargs):
        if value is None:
            return value
        init_type = type(value)
        if isinstance(value,(int)):
            value = str(value)


        if value not in _settings.datas.valid_status_codes:
            raise ValidationError(f"Invalid Status Code '{value}' [{type(init_type)}]")

        value = int(value)
        return value
