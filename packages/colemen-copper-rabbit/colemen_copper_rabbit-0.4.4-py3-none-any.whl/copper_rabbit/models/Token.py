# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import






from __future__ import annotations
from datetime import datetime
from datetime import timezone
import jwt
from typing import Iterable, List, Union
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer,Boolean
from sqlalchemy.orm import Mapped,relationship
from sqlalchemy import Column,UniqueConstraint,String,Integer,BINARY
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import sessionmaker
import colemen_utils as c


from copper_rabbit.settings.globe import base as _base
from copper_rabbit.support import format_timestamp,current_unix_timestamp
import copper_rabbit.settings as _settings



class Token(_base):
    __tablename__ = "tokens"


    token_id = Column(Integer,autoincrement=True, primary_key=True, comment='The primary key of the table.')
    tk_type = Column(String,nullable=True, default=None, comment='The type of token.')
    value = Column(String,nullable=True, default=None, comment='The tokens value that can be used as a cookie or header value.')
    expiration = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when this token will expire')
    timestamp = Column(Integer,nullable=True, default=current_unix_timestamp(), comment='The unix timestamp of when this was created.')
    deleted = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when this was deleted, null otherwise.')
    modified_timestamp = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when this was last modified, null otherwise.', onupdate=current_unix_timestamp())

    # UniqueConstraint('finger_print', name='unique_devices_fingerprint') # Ensure that the finger_print column is unique.
    UniqueConstraint('deleted','value', name='unique_tokens_value_deleted') # Ensure that the deleted,value columns are unique.

    # TODO []: TEMPORARY WHILE CREATING THE TABLES.
    role_id = Column(Integer,default=None,nullable=True )
    user_id = Column(Integer,default=None,nullable=True)    
    # session_id = Column(Integer,default=None,nullable=True)

    # TODO []: TEMPORARILY COMMENTED WHILE CREATING THE TABLES.
    # role_id = Column(Integer,ForeignKey('roles.role_id'))
    # user_id = Column(Integer,ForeignKey('users.user_id'))
    session_id = Column(Integer,ForeignKey('sessions.session_id'),nullable=True,default=None)
    # from apricity.models.InvitationsModel import InvitationsModel
    # fk_0034: Mapped[List['InvitationsModel']] = relationship(foreign_keys=[InvitationsModel.token_id_span_style_white_space_pre_span_])


    # --------------------------- CALCULATED PROPERTIES -------------------------- #
    is_expired = False
    '''True if this token's expiration timestamp is in the past.'''
    jwt = None
    '''The JWT token used to publicly represent this token.'''

    def __init__(
        self,
        token_id:int=None,
        tk_type:str=None,
        value:str=None,
        user_id:int=None,
        role_id:int=None,
        session_id:int=None,
        expiration:int=None,
        deleted:int=None,
        ) -> None:

        self.token_id = token_id
        self.user_id = user_id
        self.role_id = role_id
        self.session_id = session_id
        self.tk_type = tk_type
        if value is None:
            value = c.rand.rand(128)
        self.value = value
        if expiration is None:
            expiration = _settings.control.token_expiration + current_unix_timestamp()
        self.expiration = expiration
        self.deleted = format_timestamp(deleted,False)

        self.jwt = jwt.encode(
        payload={
            "value":value,
            "exp":expiration,
            "iss":_settings.control.token_issuer,
            # "iat":current_unix_timestamp(),
        },
        key=_settings.control.token_secret,
        algorithm=_settings.control.token_algorithm
        )
        if expiration is not None:
            if expiration <= current_unix_timestamp():
                self.is_expired = True
        

    def __repr__(self):
        return f"<TokenModel:{self.token_id}-{self.tk_type}-{self.value}>"

    def regen(self):
        print(f"REGENERATING TOKEN")
        self.value = c.rand.rand(128)
        self.expiration = _settings.control.token_expiration + current_unix_timestamp()
        # self.jwt = None
        self.jwt = jwt.encode(
        payload={
            "value":self.value,
            "exp":self.expiration,
            "iss":_settings.control.token_issuer,
            # "iat":current_unix_timestamp(),
        },
        key=_settings.control.token_secret,
        algorithm=_settings.control.token_algorithm
        )
        self.save()

    def save(self):
        _settings.globe.session.add(self)
        _settings.globe.session.commit()

    def delete(self):
        if self.token_id is not None:
            _settings.globe.session.delete(self)
            _settings.globe.session.commit()

    def soft_delete(self):
        if self.token_id is not None:
            self.deleted = current_unix_timestamp()
            _settings.globe.session.add(self)
            _settings.globe.session.commit()
            
            
            
            
            