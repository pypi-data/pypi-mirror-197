# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
import colemen_utils as c

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound

import copper_rabbit.settings as _settings
import copper_rabbit.settings.types as _t
from copper_rabbit.support.filter import get_filter as _get_filter
from copper_rabbit.support.Result import Result as _result
from copper_rabbit.support import format_timestamp,current_unix_timestamp



def new_x_from_dict(
    data,
    create_schema,
    public_schema,
    include_model:bool=True,
    )->_t._result_type:
    # find_schema_by_name()
    result = _result()
    try:
        # sess = scoped_session(sessionmaker(bind=engine))
        # @Mstep [] load the model from the data provided.
        rs = create_schema().load(data,session=_settings.globe.session)
    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        return result
    rs.save()

    result.success = True
    result.public_response = _settings.datas.successful_create_action_responses
    schema_dump = public_schema().dump(rs)
    # schema_dump = [schema_dump]

    result.set_key("schemas",[schema_dump])
    if include_model:
        result.set_key("models",[rs])

    return result

def get_x(
    model,
    public_schema,
    include_model:bool=True,
    **kwargs
    )->_t._result_type:
    result = _result()

    filter_args,kwargs = _get_filter(model,**kwargs)

    db_result = []
    try:
        db_result = []
        if len(kwargs.keys()) > 0:
            if len(filter_args) > 0:
                # @Mstep [] use the additional filter_args to search.
                db_result = _settings.globe.session.query(model).filter(*filter_args).filter_by(**kwargs)
            else:
                db_result = _settings.globe.session.query(model).filter_by(**kwargs)
        else:
            db_result = _settings.globe.session.query(model).all()
    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        return result


    result.success = True
    result.public_response = _settings.datas.successful_get_action_responses

    schema_dump = []
    models = []
    # @Mstep [LOOP] iterate the result models.
    for r in db_result:
        # print(type(r))
        models.append(r)
        rs = public_schema().dump(r)
        schema_dump.append(rs)

    result.set_key("schemas",schema_dump)
    if include_model:
        result.set_key("models",models)

    if len(schema_dump) == 0:
        result.public_response = _settings.datas.no_values_found_responses



    # result.data = out
    return result

def get_x_by_id(
    primary_id:str,
    primary_column_name:str,
    model,
    public_schema,
    include_model:bool=True,
    include_deleted:bool=False
    )->_t._result_type:
    result = _result()



    try:
        primary_id = c.string.string_decode_int(primary_id)
        args = [getattr(model,primary_column_name)==primary_id]
        if include_deleted is False:
            if hasattr(model,"deleted"):
                args.append(getattr(model,"deleted") == None)
        # raise TypeError(args)
        mdl = _settings.globe.session.query(model).filter(*args).one()
        rs = public_schema().dump(mdl)
        rs = c.obj.strip_nulls(rs)


    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        result.data = {"schemas":[]}
        return result
    except ValueError:
        result.success = False
        result.public_response = "Invalid Hash id provided."
        result.data = {"schemas":[]}
        return result
    except NoResultFound:
        result.success = False
        result.public_response = _settings.datas.no_values_found_responses
        result.data = {"schemas":[]}
        return result

    result.success = True
    result.public_response = _settings.datas.successful_get_action_responses

    if len(rs.keys()) == 1:
        rs = None
        result.public_response = _settings.datas.no_values_found_responses

    # rs = c.arr.force_list(rs,allow_nulls=False)


    result.set_key("schemas",[rs])
    if include_model is True:
        result.set_key("models",[mdl])

    # result.data = rs
    return result

def update_x(
    data,
    update_schema,
    public_schema,
    include_model:bool=True,
    )->_t._result_type:

    result = _result()
    try:
        # @Mstep [] load the model from the data provided.
        rqst = update_schema().load(data,session=_settings.globe.session)
        result_schema = public_schema().dump(rqst)
    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        return result

    rqst.save()
    # @Mstep [] add the model again, which will cause an update because the id is provided.
    # _settings.globe.session.add(rqst)
    # # @Mstep [] commit the changes.
    # _settings.globe.session.commit()

    result.success = True
    result.public_response = _settings.datas.successful_create_action_responses
    # result.data = result_schema


    result_schema = [result_schema]

    result.set_key("schemas",result_schema)
    if include_model is True:
        result.set_key("models",[rqst])


    return result

def update_col_x(
    primary_id:str,
    primary_column_name:str,
    column_name:str,
    new_value,
    model,
    public_schema,
    include_model:bool=True,
    )->_t._result_type:

    result = _result()


    # @Mstep [] retrieve the row by its id.
    try:
        primary_id = c.string.string_decode_int(primary_id)
        mdl = _settings.globe.session.query(model).filter(getattr(model,primary_column_name)==primary_id).one()
        rs = public_schema().dump(mdl)

    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        result.data = {"schemas":[]}
        return result
    except ValueError:
        result.success = False
        result.public_response = "Invalid Hash id provided."
        result.data = {"schemas":[]}
        return result
    except NoResultFound:
        result.success = False
        result.public_response = _settings.datas.no_values_found_responses
        result.data = {"schemas":[]}
        return result

    # @Mstep [] update the column
    if hasattr(mdl,column_name):
        setattr(mdl,column_name,new_value)
    # @Mstep [] save the model to the database.
    mdl.save()

    result.success = True
    result.public_response = _settings.datas.successful_update_action_responses

    result.set_key("schemas",[rs])
    if include_model is True:
        result.set_key("models",[mdl])

    # result.data = rs
    return result

def soft_delete_x(
    primary_id,
    model,
    primary_column_name:str,
    public_schema,
    include_model:bool=True,
    )->_t._result_type:
    result = _result()
    try:
        primary_id = c.string.string_decode_int(primary_id)
        mdl = _settings.globe.session.query(model).filter(getattr(model,primary_column_name)==primary_id).one()
        # raise TypeError(mdl)

    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        return result

    except NoResultFound:
        result.success = False
        result.public_response = _settings.datas.no_values_found_responses
        result.data = {"schemas":[]}
        return result
    except ValueError:
        result.success = False
        result.public_response = "Invalid Hash ID provided"
        result.data = {"schemas":[]}
        return result

    mdl.deleted = current_unix_timestamp()
    mdl.save()
    rs = public_schema().dump(mdl)


    rs = c.arr.force_list(rs,allow_nulls=False)


    result.set_key("schemas",rs)
    if include_model is True:
        result.set_key("models",mdl)

    result.success = True
    result.public_response = "Deleted!"
    # result.data = rs
    return result

def undo_soft_delete_x(
    primary_id,
    model,
    primary_column_name:str,
    public_schema,
    include_model:bool=True,
    )->_t._result_type:
    result = _result()
    try:

        primary_id = c.string.string_decode_int(primary_id)
        # raise TypeError(primary_id)
        mdl = _settings.globe.session.query(model).filter(getattr(model,primary_column_name)==primary_id).one()
        # raise TypeError(mdl)

    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        result.data = {"schemas":[]}
        return result

    except NoResultFound:
        result.success = False
        result.public_response = _settings.datas.no_values_found_responses
        result.data = {"schemas":[]}
        return result



    mdl.deleted = None
    mdl.save()
    rs = public_schema().dump(mdl)


    # rs = c.arr.force_list(rs,allow_nulls=False)


    result.set_key("schemas",[rs])
    if include_model is True:
        result.set_key("models",[mdl])

    result.success = True
    result.public_response = _settings.datas.successful_create_action_responses
    # result.data = rs
    return result

def delete_x(
    primary_id,
    model,
    primary_column_name:str,
    public_schema,
    include_model:bool=True,
    )->_t._result_type:
    result = _result()
    try:

        primary_id = c.string.string_decode_int(primary_id)
        mdl = _settings.globe.session.query(model).filter(getattr(model,primary_column_name)==primary_id).one()

    except ValidationError as e:
        result.success = False
        result.public_response = _settings.datas.validation_errors_public_responses
        result.add_error(e.messages)
        return result
    except NoResultFound:
        result.success = False
        result.public_response = _settings.datas.no_values_found_responses
        result.data = {"schemas":[]}
        return result

    mdl.delete()
    rs = public_schema().dump(mdl)

    rs = c.arr.force_list(rs,allow_nulls=False)


    result.set_key("schemas",rs)
    if include_model is True:
        result.set_key("models",mdl)

    result.success = True
    result.public_response = "Deleted!"
    # result.data = rs
    return result


















