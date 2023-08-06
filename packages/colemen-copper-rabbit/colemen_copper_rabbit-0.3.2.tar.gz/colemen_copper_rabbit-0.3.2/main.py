# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import json
# from typing import Union
import colemen_utils as _c
# from sqlalchemy.orm import Session
from sqlalchemy import create_engine as _create_engine
# from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker as _sessionmaker
from sqlalchemy.orm import scoped_session
from copper_rabbit.support.gen_mysql_connection_url import gen_mysql_connection_url as _mysql_url

import copper_rabbit.settings as _settings

def create_session(url:str=None,app=None):
    import copper_rabbit.settings.globe as _globe
    if app is not None:
        _ge = _c.build.get_environ

        if "sqlite" in _ge(app.config["DEFAULT_DATABASE"]):
            _globe.engine = _ge(app.config["DEFAULT_DATABASE"])
        if "mysql" in _ge(app.config["DEFAULT_DATABASE"]):
            app.config['SQLALCHEMY_DATABASE_URI'] = _mysql_url(_ge(app.config["DEFAULT_DATABASE"]))
            
            app.config["SQLALCHEMY_BINDS"] = {
                "management_database":_mysql_url(data=_ge("MANAGEMENT_CREDS")),
                "meta_database":_mysql_url(data=_ge("META_CREDS")),
                "business_database":_mysql_url(data=_ge("BUSINESS_CREDS")),
            }
            _create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    else:
        if url is None:
            url = "sqlite:///test.db"
        _globe.engine = _create_engine(url)


    _Session = scoped_session(_sessionmaker(bind=_globe.engine))

    _globe.session = _Session()
    _globe.base.metadata.create_all(_globe.engine)




import copper_rabbit.models as _models
import copper_rabbit.schemas as _schemas
import copper_rabbit.actions as act