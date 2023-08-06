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
from sqlalchemy.orm import Mapped,relationship
from sqlalchemy import Column,UniqueConstraint,String,Integer,BINARY
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import sessionmaker
import colemen_utils as c


from copper_rabbit.settings.globe import base as _base
from copper_rabbit.support import format_timestamp,current_unix_timestamp
import copper_rabbit.settings as _settings
# from minimal_nova.models.LogTags import log_tags_table
# from minimal_nova.models.Tags import Tags
# from minimal_nova.models.TagAliases import TagAliases



class Device(_base):
    __tablename__ = "devices"

    # session_hash = Column(String,comment='The has value that can be used in the cookie/header for identifying this session.')
    # last_activity_timestamp = Column(Integer,nullable=True, default=None, onupdate=current_unix_timestamp(), comment='Unix timestamp of the last time this session performed an activity.')
    # invalidated = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when the session was invalidated.')
    # expired = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when the session was determined to be expired.')


    device_id = Column(Integer,autoincrement=True, primary_key=True, comment='The primary key of the table.')
    finger_print = Column(String(255),comment='The devices fingerprint hash')
    screen_width = Column(Integer,nullable=True, default=None, comment='The width of the device screen in pixels')
    screen_height = Column(Integer,nullable=True, default=None, comment='The height of the device screen in pixels')
    full_version = Column(String(100),nullable=True, default=None, comment='The full version of the browser')
    major_version = Column(String(100),nullable=True, default=None, comment='The major version of the browser')
    os = Column(String(255),nullable=True, default=None, comment='The name of the operating system.')
    os_version = Column(String(255),nullable=True, default=None, comment='The version of the operating system')
    timestamp = Column(Integer,nullable=True, default=current_unix_timestamp(), comment='The unix timestamp of when this was created.')
    deleted = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when this was deleted, null otherwise.')
    modified_timestamp = Column(Integer,nullable=True, default=current_unix_timestamp(), onupdate=current_unix_timestamp(), comment='The unix timestamp of when this was last modified, null otherwise.')




    UniqueConstraint('finger_print', name='unique_devices_fingerprint') # Ensure that the finger_print column is unique.



    def __init__(
        self,
        device_id:int=None,
        finger_print:str=None,
        screen_width:int=None,
        screen_height:int=None,
        full_version:str=None,
        major_version:str=None,
        os:str=None,
        os_version:str=None,
        deleted:int=None,
        ) -> None:

        self.device_id = device_id
        self.finger_print = finger_print
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.full_version = full_version
        self.major_version = major_version
        self.os = os
        self.os_version = os_version
        self.deleted = format_timestamp(deleted,False)


    def __repr__(self):
        return f"<DeviceModel:{self.device_id}-{self.finger_print}>"


    def save(self):
        _settings.globe.session.add(self)
        _settings.globe.session.commit()

    def delete(self):
        if self.device_id is not None:
            _settings.globe.session.delete(self)
            _settings.globe.session.commit()