# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import






from __future__ import annotations
# from datetime import datetime
# from datetime import timezone
# import re
from typing import Iterable, List, Union
# from sqlalchemy.orm import Column
# from sqlalchemy import ForeignKey

# from sqlalchemy.orm import Mapped
# from sqlalchemy import Column,String,Integer
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import sessionmaker
# from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields, validate, ValidationError,EXCLUDE
import colemen_utils as c


# from copper_rabbit.settings.globe import base as _base
import copper_rabbit.settings as _settings
from copper_rabbit.models.Request import Request
from copper_rabbit.custom_fields import StatusCode,CrudType,RequestMethod,RequestLog,HashidPrimary,DeletedTimestamp
from copper_rabbit.support.BaseSchema import BaseSchema


class CreateRequestSchema(BaseSchema):
    class Meta:
        model = Request
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE

    description = fields.Str(validate=[validate.Length(None,500)])
    crud_type = CrudType(default=None,allow_none=True)
    status_code = StatusCode(default=None,allow_none=True)
    ra_success = fields.Bool(default=None,allow_none=True)
    log = RequestLog(default=None,allow_none=True)
    host_name = fields.Str(default=None,allow_none=True)
    ip_address = fields.Str(default=None,allow_none=True)
    user_agent = fields.Str(default=None,allow_none=True)
    request_uri = fields.Str(validate=validate.URL(),default=None,allow_none=True)
    protocol = fields.Str(validate=validate.OneOf(["http","https"]),default=None,allow_none=True)
    method = RequestMethod(default=None,allow_none=True)
    timestamp = fields.Int(dump_only=True)
    deleted = fields.Int(dump_only=True)
    modified_timestamp = fields.Int(dump_only=True)


    def __repr__(self):
        return f"<{self.class_name}:{self.method}-{self.crud_type}-{self.protocol}-{self.ip_address}-{self.description}>"

class PublicRequestSchema(BaseSchema):
    class Meta:
        model = Request
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE

    request_id = HashidPrimary()
    description = fields.Str(validate=[validate.Length(None,500)])
    crud_type = CrudType(default=None,allow_none=True)
    status_code = StatusCode(default=None,allow_none=True)
    ra_success = fields.Bool(default=None,allow_none=True)
    log = RequestLog(default=None,allow_none=True)
    host_name = fields.Str(default=None,allow_none=True)
    ip_address = fields.Str(default=None,allow_none=True)
    user_agent = fields.Str(default=None,allow_none=True)
    request_uri = fields.Str(validate=validate.URL(),default=None,allow_none=True)
    protocol = fields.Str(validate=validate.OneOf(["http","https"]),default=None,allow_none=True)
    method = RequestMethod(default=None,allow_none=True)
    timestamp = fields.Int(dump_only=True)
    deleted = fields.Int(dump_only=True)
    modified_timestamp = fields.Int(dump_only=True)

    request_hash = fields.Str(dump_only=True)


    def __repr__(self):
        return f"<{self.class_name}:{self.request_id}-{self.crud_type}-{self.protocol}-{self.ip_address}-{self.description}>"

class GetRequestSchema(BaseSchema):
    class Meta:
        model = Request
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE

    request_id = HashidPrimary()
    description = fields.Str(validate=[validate.Length(None,500)])
    crud_type = CrudType(default=None,allow_none=True)
    status_code = StatusCode(default=None,allow_none=True)
    ra_success = fields.Bool(default=None,allow_none=True)
    log = RequestLog(default=None,allow_none=True)
    host_name = fields.Str(default=None,allow_none=True)
    ip_address = fields.Str(default=None,allow_none=True)
    user_agent = fields.Str(default=None,allow_none=True)
    request_uri = fields.Str(validate=validate.URL(),default=None,allow_none=True)
    protocol = fields.Str(validate=validate.OneOf(["http","https"]),default=None,allow_none=True)
    method = RequestMethod(default=None,allow_none=True)
    timestamp = fields.Int(dump_only=True)
    deleted = fields.Int(dump_only=True)
    modified_timestamp = fields.Int(dump_only=True)


    def __repr__(self):
        return f"<{self.class_name}:{self.request_id}-{self.crud_type}-{self.protocol}-{self.ip_address}-{self.description}>"

class UpdateRequestSchema(BaseSchema):
    class Meta:
        model = Request
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE

    request_id = HashidPrimary(required=True)
    description = fields.Str(validate=[validate.Length(None,500)])
    crud_type = CrudType(default=None,allow_none=True)
    status_code = StatusCode(default=None,allow_none=True)
    ra_success = fields.Bool(default=None,allow_none=True)
    log = RequestLog(default=None,allow_none=True)
    host_name = fields.Str(default=None,allow_none=True)
    ip_address = fields.Str(default=None,allow_none=True)
    user_agent = fields.Str(default=None,allow_none=True)
    request_uri = fields.Str(validate=validate.URL(),default=None,allow_none=True)
    protocol = fields.Str(validate=validate.OneOf(["http","https"]),default=None,allow_none=True)
    method = RequestMethod(default=None,allow_none=True)
    timestamp = fields.Int(dump_only=True)
    deleted = fields.Int(dump_only=True)
    modified_timestamp = fields.Int(dump_only=True)


    def __repr__(self):
        return f"<{self.class_name}:{self.request_id}-{self.crud_type}-{self.protocol}-{self.ip_address}-{self.description}>"

class SoftDeleteRequestSchema(BaseSchema):
    class Meta:
        model = Request
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE

    request_id = HashidPrimary(required=True)
    deleted = DeletedTimestamp(required=True,allow_none=True)
    modified_timestamp = fields.Int(dump_only=True)


    def __repr__(self):
        return f"<{self.class_name}:{self.request_id}-{self.deleted}-{self.modified_timestamp}>"

class DeleteRequestSchema(BaseSchema):
    class Meta:
        model = Request
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE

    request_id = HashidPrimary(required=True)


    def __repr__(self):
        return f"<{self.class_name}:{self.request_id}>"


