# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from typing import Union
import colemen_utils as _c
from marshmallow import Schema, fields, validate, ValidationError
import copper_rabbit.settings as _settings

class HashidPrimary(fields.Field):
    """Field that serializes an integer and deserializes to an encoded version of the integer."""

    def _serialize(self, value:Union[int,str], attr, obj, **kwargs):
        if value is None:
            return value
        if isinstance(value,(int)) is False:
            raise ValidationError(f"Invalid Primary ID '{value}' [{type(value)}] - expected an integer.")


        value = _c.string.string_encode_int(value)

        return value


    def _deserialize(self, value:int, attr, data, **kwargs):

        if value is None:
            return None
        # if isinstance(value,(int)):
        #     return value

        if isinstance(value,(str)) is False:
            raise ValidationError(f"Invalid Hash ID '{value}' [{type(value).__name__}] - expected a string.")
        try:
            value = _c.string.string_decode_int(value)
            # raise ValueError(value)
            if isinstance(value,(int)) is False:
                raise ValidationError(f"Invalid Hash ID '{value}' [{type(value).__name__}]")
        except ValueError:
            raise ValidationError(f"Invalid Hash ID '{value}' [{type(value).__name__}]")
            
        return value