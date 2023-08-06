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
from copper_rabbit.models.Session import Session
from copper_rabbit.custom_fields import HashidPrimary,DeletedTimestamp
from copper_rabbit.support.BaseSchema import BaseSchema


class CreateSessionSchema(BaseSchema):
    '''Schema used for creating a session'''
    class Meta:
        model = Session
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE


    session_hash = fields.Str(nullable=True, default=None)
    last_activity_timestamp = fields.Int(dump_only=True)
    invalidated = fields.Int(dump_only=True)
    expired = fields.Int(nullable=True,default=None,dump_only=True)
    timestamp = fields.Int(dump_only=True)
    deleted = fields.Int(dump_only=True)
    modified_timestamp = fields.Int(dump_only=True)

    def __repr__(self):
        return f"<{self.class_name}:{self.session_hash}>"

class PublicSessionSchema(BaseSchema):
    '''Schema used for filtering what is publicly visible about a session'''
    class Meta:
        model = Session
        include_relationships = True
        load_instance = True
        unknown=EXCLUDE

    session_id = HashidPrimary()
    last_activity_timestamp = fields.Int(dump_only=True)
    invalidated = fields.Int(dump_only=True)
    expired = fields.Int(nullable=True,default=None,dump_only=True)
    timestamp = fields.Int(dump_only=True)
    deleted = fields.Int(dump_only=True)
    modified_timestamp = fields.Int(dump_only=True)



    def __repr__(self):
        return f"<{self.class_name}:{self.last_activity_timestamp}-{self.expired}>"

# class GetSessionSchema(BaseSchema):
#     '''Schema that defines the searchable "get" parameters of a session'''
#     class Meta:
#         model = Session
#         include_relationships = True
#         load_instance = True
#         unknown=EXCLUDE

#     session_id = HashidPrimary()
#     expiration = fields.Int(nullable=True,default=None)
#     tk_type = fields.Str(nullable=True, default=None)
#     value = fields.Str(nullable=True, default=None)

#     timestamp = fields.Int(dump_only=True)
#     deleted = fields.Int(dump_only=True)
#     modified_timestamp = fields.Int(dump_only=True)


#     def __repr__(self):
#         return f"<{self.class_name}:{self.tk_type}-{self.expiration}>"

# class UpdateSessionSchema(BaseSchema):
#     '''Schema that defines the columns of a session that can be updated.

#     Only the expiration timestamp can be updated.

#     '''
#     class Meta:
#         model = Session
#         include_relationships = True
#         load_instance = True
#         unknown=EXCLUDE

#     session_id = HashidPrimary(required=True,dump_only=True)
#     expiration = fields.Int(nullable=True,default=None)
#     timestamp = fields.Int(dump_only=True)
#     deleted = fields.Int(dump_only=True)
#     modified_timestamp = fields.Int(dump_only=True)


#     def __repr__(self):
#         return f"<{self.class_name}:{self.expiration}>"

# class SoftDeleteSessionSchema(BaseSchema):
#     '''Schema used for soft deleting a session'''
#     class Meta:
#         model = Session
#         include_relationships = True
#         load_instance = True
#         unknown=EXCLUDE

#     session_id = HashidPrimary(required=True)
#     deleted = DeletedTimestamp(required=True,allow_none=True)
#     modified_timestamp = fields.Int(dump_only=True)


#     def __repr__(self):
#         return f"<{self.class_name}:{self.session_id}>"

# class DeleteSessionSchema(BaseSchema):
#     '''Schema used for permanently deleting a session.'''
#     class Meta:
#         model = Session
#         include_relationships = True
#         load_instance = True
#         unknown=EXCLUDE

#     session_id = HashidPrimary(required=True)
#     value = fields.Str(nullable=True,defualt=None)


#     def __repr__(self):
#         return f"<{self.class_name}:{self.session_id}>"


