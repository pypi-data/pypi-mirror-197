# # pylint: disable=missing-function-docstring
# # pylint: disable=missing-class-docstring
# # pylint: disable=line-too-long
# # pylint: disable=unused-import






# from __future__ import annotations
# from datetime import datetime
# from datetime import timezone
# import re
# from typing import Iterable, List, Union
# from sqlalchemy.orm import mapped_column
# from sqlalchemy import ForeignKey
# from sqlalchemy import Integer,Boolean
# from sqlalchemy.orm import Mapped
# from sqlalchemy import Column,String,Integer
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import sessionmaker
from typing import Iterable, Union
import colemen_utils as c
import copper_rabbit.settings as _settings
import copper_rabbit.settings.types as _t
from copper_rabbit.support.filter import get_filter as _get_filter
from copper_rabbit.support.Result import Result as _result
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound

# from copper_rabbit.settings.globe import base as _base
# from copper_rabbit.support import format_timestamp,current_unix_timestamp
# # from minimal_nova.models.LogTags import log_tags_table
# # from minimal_nova.models.Tags import Tags
# # from minimal_nova.models.TagAliases import TagAliases
import copper_rabbit.schemas.Request as _schemas
from copper_rabbit.models.Request import Request as _model

def new_from_dict(data)->_t._result_type:
    '''
        Create a new request log
        ----------

        Arguments
        -------------------------
        `data` {dict}
            A dictionary of data for creating the request log.

        Return {Request}
        ----------------------
        The request model if successful.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 13:37:43
        `memberOf`: Request
        `version`: 1.0
        `method_name`: new
        * @xxx [03-15-2023 13:44:50]: documentation for new
    '''
    result = _result()
    try:
        # @Mstep [] load the model from the data provided.
        rs:_model = _schemas.CreateRequestSchema().load(data)
    except ValidationError as e:
        result.success = False
        result.public_response = "Correct the errors and try again."
        result.add_error(e.messages)
        return result
    rs.save()

    result.success = True
    result.public_response = "Here is the stuff"
    result.data = _schemas.PublicRequestSchema().dump(rs)
    # _settings.globe.session.add(rs)
    # _settings.globe.session.commit()
    return result

def get(**kwargs)->_t._result_type:
    result = _result()
# def get(**kwargs)->Union[Iterable[_model],_model]:
    filter_args,kwargs = _get_filter(_model,**kwargs)
    db_result = []
    try:
        db_result = []
        if len(kwargs.keys()) > 0:
            if len(filter_args) > 0:
                db_result = _settings.globe.session.query(_model).filter(*filter_args).filter_by(**kwargs)
            else:
                db_result = _settings.globe.session.query(_model).filter_by(**kwargs)
        else:
            db_result = _settings.globe.session.query(_model).all()
    except ValidationError as e:
        result.success = False
        result.public_response = "Correct the errors and try again."
        result.add_error(e.messages)
        return result

    out = []
    for r in db_result:
        rs = _schemas.PublicRequestSchema().dump(r)
        out.append(rs)

    result.success = True
    result.public_response = "Here is the stuff"
    result.data = out
    return result

def get_by_id(request_id:str)->_t._result_type:
    result = _result()
    try:
        request_id = c.string.string_decode_int(request_id)
        
        rqst = _settings.globe.session.query(_model).filter(_model.request_id==request_id).one()
        rs = _schemas.PublicRequestSchema().dump(rqst)
        rs = c.obj.strip_nulls(rs)


    except ValidationError as e:
        result.success = False
        result.public_response = "Correct the errors and try again."
        result.add_error(e.messages)
        result.data = None
        return result
    except ValueError:
        result.success = False
        result.public_response = "Invalid Hash id provided."
        result.data = None
        return result
    except NoResultFound:
        result.success = False
        result.public_response = "Nothing to see here"
        result.data = []
        return result
    
    if len(rs.keys()) == 1:
        rs = None
    
    result.success = True
    result.public_response = "Here is the stuff"
    result.data = rs
    return result

def update(data)->_t._result_type:
    result = _result()
    try:
        # @Mstep [] load the model from the data provided.
        rqst = _schemas.UpdateRequestSchema().load(data)
        result_schema = _schemas.PublicRequestSchema().dump(rqst)
    except ValidationError as e:
        result.success = False
        result.public_response = "Correct the errors and try again."
        result.add_error(e.messages)
        return result

    # @Mstep [] add the model again, which will cause an update because the id is provided.
    _settings.globe.session.add(rqst)
    # @Mstep [] commit the changes.
    _settings.globe.session.commit()

    result.success = True
    result.public_response = "Saved!"
    result.data = result_schema
    # rs = _schemas.PublicRequestSchema().dump(rqst)
    return result

def soft_delete(data)->_t._result_type:
    result = _result()
    try:
        result = get_by_id(data['request_id'])
        if result.success is False:
            result.success = False
            result.public_response = "Correct the errors and try again."
            result.add_error("request_id","Invalid hash id provided.")
            return result

        # @Mstep [] load the model from the data provided.
        rqst = _schemas.SoftDeleteRequestSchema().load(data)
        rs = _schemas.PublicRequestSchema().dump(rqst)
    except ValidationError as e:
        result.success = False
        result.public_response = "Correct the errors and try again."
        result.add_error(e.messages)
        return result

    # @Mstep [] add the model again, which will cause an update because the id is provided.
    _settings.globe.session.add(rqst)
    # @Mstep [] commit the changes.
    _settings.globe.session.commit()
    
    
    result.success = True
    result.public_response = "Deleted!"
    result.data = rs
    return result

def undo_soft_delete(data)->_t._result_type:
    result = _result()
    try:
    # @Mstep [] load the model from the data provided.
        rqst = _schemas.SoftDeleteRequestSchema().load(data)
        result_schema = _schemas.PublicRequestSchema().dump(rqst)
    except ValidationError as e:
        result.success = False
        result.public_response = "Correct the errors and try again."
        result.add_error(e.messages)
        return result
    # @Mstep [] add the model again, which will cause an update because the id is provided.
    _settings.globe.session.add(rqst)
    # @Mstep [] commit the changes.
    _settings.globe.session.commit()
    result.success = True
    result.public_response = "Saved!"
    result.data = result_schema
    return result

def delete(data)->_t._result_type:
    result = _result()
    try:
        # @Mstep [] load the model from the data provided.
        rqst = _schemas.DeleteRequestSchema().load(data)
        result_schema = _schemas.PublicRequestSchema().dump(rqst)
    except ValidationError as e:
        result.success = False
        result.public_response = "Correct the errors and try again."
        result.add_error(e.messages)
        return result
    # @Mstep [] add the model again, which will cause an update because the id is provided.
    _settings.globe.session.delete(rqst)
    # @Mstep [] commit the changes.
    _settings.globe.session.commit()
    result.success = True
    result.public_response = "Deleted!"
    result.data = result_schema
    return result