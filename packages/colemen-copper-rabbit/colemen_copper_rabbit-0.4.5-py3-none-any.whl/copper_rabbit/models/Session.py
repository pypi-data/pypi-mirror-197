# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import






from __future__ import annotations
from datetime import datetime
from datetime import timezone
import re
from typing import Iterable, List, Union
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer,Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy import Column,String,Integer,BINARY
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import colemen_utils as c


from copper_rabbit.settings.globe import base as _base
from copper_rabbit.support import format_timestamp,current_unix_timestamp
from copper_rabbit.models.Token import Token as _Token
# from copper_rabbit.actions.Token import new_from_dict as _new_token
import copper_rabbit.settings as _settings




class Session(_base):
    __tablename__ = "sessions"

    session_id = Column(Integer,autoincrement=True, primary_key=True, comment='The primary key of the table.')
    session_hash = Column(String,comment='The has value that can be used in the cookie/header for identifying this session.')
    last_activity_timestamp = Column(Integer,nullable=True, default=None, onupdate=current_unix_timestamp(), comment='Unix timestamp of the last time this session performed an activity.')
    invalidated = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when the session was invalidated.')
    expired = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when the session was determined to be expired.')
    timestamp = Column(Integer,nullable=True, default=current_unix_timestamp(), comment='The unix timestamp of when this was created.')
    deleted = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when this was deleted, null otherwise.')
    modified_timestamp = Column(Integer,nullable=True, default=current_unix_timestamp(), onupdate=current_unix_timestamp(), comment='The unix timestamp of when this was last modified, null otherwise.')

    # token_id: Mapped[int] = mapped_column(ForeignKey("tokens.token_id"))
    tokens: Mapped[List["Token"]] = relationship()



    def __init__(
        self,
        session_id:int=None,
        session_hash:str=None,
        last_activity_timestamp:int=None,
        invalidated:int=None,
        expired:int=None,
        deleted:int=None,
        ) -> None:

        self.session_id = session_id
        self.session_hash = session_hash
        self.last_activity_timestamp = last_activity_timestamp
        self.invalidated = invalidated
        self.expired = expired
        self.deleted = format_timestamp(deleted,False)


    def gen_token(self):
        if self.session_id is None:
            self.save()
        tk = _Token(
            tk_type="access",
            session_id=self.session_id
        )
        tk.save()
    def __repr__(self):
        return f"<SessionModel:{self.session_id}-{self.session_hash}>"


    def save(self):
        _settings.globe.session.add(self)
        _settings.globe.session.commit()

    def delete(self):
        if self.session_id is not None:
            _settings.globe.session.delete(self)
            _settings.globe.session.commit()

    def soft_delete(self):
        if self.token_id is not None:
            self.deleted = current_unix_timestamp()
            _settings.globe.session.add(self)
            _settings.globe.session.commit()


