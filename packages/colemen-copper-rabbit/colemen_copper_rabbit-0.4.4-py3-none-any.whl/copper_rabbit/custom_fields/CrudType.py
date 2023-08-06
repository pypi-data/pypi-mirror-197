# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from typing import Union
import colemen_utils as _c
from marshmallow import Schema, fields, validate, ValidationError
import copper_rabbit.settings as _settings

class CrudType(fields.Field):
    """Field that serializes a crud operation type using aliases."""

    def _serialize(self, value:Union[int,str], attr, obj, **kwargs):
        if value is None:
            return None

        if value not in _settings.datas.valid_crud_types:
            return None

        return value

    def _deserialize(self, value:Union[int,str], attr, data, **kwargs):
        if value is None:
            return value

        valid_value = _c.valid.crud_type(value)


        if valid_value is False:
            raise ValidationError(f"Invalid CRUD type '{value}' - expected: [{', '.join(_settings.datas.valid_crud_types)}]")

        return value
