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
from sqlalchemy.orm import relationship,column_property
from sqlalchemy.orm import sessionmaker
import colemen_utils as c


from copper_rabbit.settings.globe import base as _base
from copper_rabbit.support import format_timestamp,current_unix_timestamp
import copper_rabbit.settings as _settings
# from minimal_nova.models.LogTags import log_tags_table
# from minimal_nova.models.Tags import Tags
# from minimal_nova.models.TagAliases import TagAliases



class Request(_base):
    __tablename__ = "requests"

    # TODO []: add the session_id and device_id columns
    request_id = Column(Integer,primary_key=True,autoincrement=True)

    description = Column(String(500),nullable=True, default=None, comment='A brief description of the request')
    crud_type = Column(String(50),nullable=True, default=None, comment='The crud operation performed on this request.')
    status_code = Column(String(50),nullable=True, default=None, comment='The status code of the response to this request.')
    ra_success = Column(Boolean(50),nullable=True, default=0, comment='The Result objects success value, this indicates if the operation itself was successful.')
    log = Column(BINARY,nullable=True, default=None, comment='The compressed request log for this request')
    host_name = Column(String(255),nullable=True, default=None, comment='The host name from the request.')
    ip_address = Column(String(255),nullable=True, default=None, comment='The ip_address from the request.')
    user_agent = Column(String(255),nullable=True, default=None, comment='The user agent from the request.')
    request_uri = Column(String(500),nullable=True, default=None, comment='The URI from the request.')
    protocol = Column(String(50),nullable=True, default=None, comment='The protocol from the request.')
    method = Column(String(50),nullable=True, default=None, comment='The method used from the request.')
    timestamp = Column(Integer,nullable=True, default=current_unix_timestamp(), comment='The unix timestamp of when this was created.')
    deleted = Column(Integer,nullable=True, default=None, comment='The unix timestamp of when this was deleted, null otherwise.')
    modified_timestamp = Column(Integer,nullable=True, default=current_unix_timestamp(), comment='The unix timestamp of when this was last modified, null otherwise.', onupdate=current_unix_timestamp())

    # session_id = Column(Integer,ForeignKey('sessions.session_id'))
    # device_id = Column(Integer,ForeignKey('devices.device_id'))
    # from apricity.models.ActivityLogsModel import ActivityLogsModel
    # fk_0028: Mapped[List['ActivityLogsModel']] = relationship(foreign_keys=[ActivityLogsModel.request_id])


    # --------------------------- CALCULATED PROPERTIES -------------------------- #
    request_hash = c.string.to_hash(f"{crud_type}_{status_code}_{ip_address}_{protocol}_{method}_{timestamp}")



    def __init__(
        self,
        request_id:int=None,
        description:str=None,
        status_code:str=None,
        crud_type:str=None,
        ra_success:str=None,
        log:str=None,
        host_name:str=None,
        ip_address:str=None,
        user_agent:str=None,
        request_uri:str=None,
        protocol:str=None,
        method:str=None,
        deleted=None,
        ) -> None:

        self.request_id = request_id
        self.description = description
        self.crud_type = crud_type
        self.status_code = status_code
        self.ra_success = ra_success
        self.log = log
        self.host_name = host_name
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.request_uri = request_uri
        self.protocol = protocol
        self.method = method
        self.deleted = format_timestamp(deleted,False)


    def __repr__(self):
        return f"<Request_model:{self.request_id}-{self.method}-{self.crud_type}-{self.protocol}-{self.ip_address}-{self.description}>"


    def save(self):
        _settings.globe.session.add(self)
        _settings.globe.session.commit()

    def delete(self):
        if self.request_id is not None:
            _settings.globe.session.delete(self)
            _settings.globe.session.commit()