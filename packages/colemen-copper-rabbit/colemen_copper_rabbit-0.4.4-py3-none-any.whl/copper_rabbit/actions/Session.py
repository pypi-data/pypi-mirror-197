# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The Session action methods

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 03-16-2023 09:53:46
    `name`: Session
    * @xxx [03-16-2023 09:54:06]: documentation for Session
'''


import colemen_utils as _c
import jwt
from sqlalchemy.exc import NoResultFound


import copper_rabbit.settings as _settings
import copper_rabbit.settings.types as _t
import copper_rabbit.schemas.Session as _schemas
from copper_rabbit.support.Result import Result as _result
from copper_rabbit.models.Session import Session as _model
import copper_rabbit.support.actions as _x
from copper_rabbit.support import format_timestamp,current_unix_timestamp

_PRIMARY_COLUMN_NAME="session_id"
_DEFAULT_PUBLIC_SCHEMA=_schemas.PublicSessionSchema
_DEFAULT_CREATE_SCHEMA=_schemas.CreateSessionSchema
# _DEFAULT_UPDATE_SCHEMA=_schemas.UpdateSessionSchema



def new_from_dict(data=None,include_model:bool=True)->_t._result_type:
    '''
        Create a new session log
        ----------

        Arguments
        -------------------------
        `data` {dict}
            A dictionary of data for creating a new session.

        Return {Result}
        ----------------------
        A Result instance.

        {
            success:True/False,
            public_response:"Here is the stuff",
            errors:{},
            data:{
                "public":[],
                "model":SessionModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 13:37:43
        `memberOf`: Session
        `version`: 1.0
        `method_name`: new
        * @xxx [03-15-2023 13:44:50]: documentation for new
    '''
    if data is None:
        data = {}
    data['session_hash'] = _c.rand.rand(128)
    result = _x.new_x_from_dict(
        data,
        _DEFAULT_CREATE_SCHEMA,
        _DEFAULT_PUBLIC_SCHEMA,
        include_model=True,
    )

    if result.success is True:
        result.models.gen_token()

    return result

def get_by_id(primary_id:str,include_model:bool=False,include_deleted:bool=False)->_t._result_type:
    '''
        Retrieve a session by its id.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded session_id to search for.

        [`include_model`=True] {bool}
            Add the "models" key to the result data.



        Return {Result}
        ----------------------
        A Result instance.

        {
            success:True/False,
            public_response:"Here is the stuff",
            errors:{},
            data:{
                "public":[
                    {PublicSessionSchema}
                ],
                "model":SessionModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-16-2023 11:55:48
        `version`: 1.0
        `method_name`: get_by_id
        * @xxx [03-16-2023 11:57:25]: documentation for get_by_id
    '''
    return _x.get_x_by_id(
        primary_id=primary_id,
        primary_column_name=_PRIMARY_COLUMN_NAME,
        model=_model,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
        include_deleted=include_deleted,
        )

# def regen_session(primary_id:str):
#     result = _x.get_x_by_id(
#         primary_id=primary_id,
#         primary_column_name=_PRIMARY_COLUMN_NAME,
#         model=_model,
#         public_schema=_DEFAULT_PUBLIC_SCHEMA,
#     )
#     if result.success is True:
#         result.models[0].regen()
#         # mdl.regen()

#     result = _x.get_x_by_id(
#         primary_id=primary_id,
#         primary_column_name=_PRIMARY_COLUMN_NAME,
#         model=_model,
#         public_schema=_DEFAULT_PUBLIC_SCHEMA,
#     )

#     return result

def purge_expired():
    '''Delete all sessions that have an expired timestamp'''

    models = _settings.globe.session.query(_model).filter((current_unix_timestamp() - _model.expired) >= 86400).all()
    for m in models:
        m.soft_delete()

# def update(data:dict,include_model:bool=False)->_t._result_type:
#     '''
#         update a session.
#         ----------

#         Arguments
#         -------------------------
#         `data` {dict}
#             A dictionary of data to update the session with.

#         [`include_model`=True] {bool}
#             Add the "models" key to the result data.



#         Return {Result}
#         ----------------------
#         A Result instance.

#         {
#             success:True/False,
#             public_response:"Here is the stuff",
#             errors:{},
#             data:{
#                 "public":[
#                     {PublicSessionSchema}
#                 ],
#                 "model":SessionModel,
#             },
#         }

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 03-16-2023 11:55:48
#         `version`: 1.0
#         `method_name`: update
#         * @xxx [03-16-2023 11:57:25]: documentation for update
#     '''
#     return _x.update_x(
#         data,
#         update_schema=_DEFAULT_UPDATE_SCHEMA,
#         public_schema=_DEFAULT_PUBLIC_SCHEMA,
#         include_model=include_model,
#         )

def soft_delete(primary_id:str,include_model:bool=False)->_t._result_type:
    '''
        Soft delete a session.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded session_id to search for.

        [`include_model`=True] {bool}
            Add the "models" key to the result data.



        Return {Result}
        ----------------------
        A Result instance.

        {
            success:True/False,
            public_response:"Here is the stuff",
            errors:{},
            data:{
                "public":[
                    {PublicSessionSchema}
                ],
                "model":SessionModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-16-2023 11:55:48
        `version`: 1.0
        `method_name`: soft_delete
        * @xxx [03-16-2023 11:57:25]: documentation for soft_delete
    '''
    return _x.soft_delete_x(
        primary_id=primary_id,
        model=_model,
        primary_column_name=_PRIMARY_COLUMN_NAME,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
        )

def undo_soft_delete(primary_id:str,include_model:bool=False)->_t._result_type:
    '''
        Undo the Soft deletion of a session.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded session_id to search for.

        [`include_model`=True] {bool}
            Add the "models" key to the result data.



        Return {Result}
        ----------------------
        A Result instance.

        {
            success:True/False,
            public_response:"Here is the stuff",
            errors:{},
            data:{
                "public":[
                    {PublicSessionSchema}
                ],
                "model":SessionModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-16-2023 11:55:48
        `version`: 1.0
        `method_name`: undo_soft_delete
        * @xxx [03-16-2023 11:57:25]: documentation for undo_soft_delete
    '''
    return _x.undo_soft_delete_x(
        primary_id=primary_id,
        model=_model,
        primary_column_name=_PRIMARY_COLUMN_NAME,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
        )

def delete(primary_id:str,include_model:bool=False)->_t._result_type:
    '''
        Permanently delete a session
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded session_id to search for.

        [`include_model`=True] {bool}
            Add the "models" key to the result data.



        Return {Result}
        ----------------------
        A Result instance.

        {
            success:True/False,
            public_response:"Here is the stuff",
            errors:{},
            data:{
                "public":[
                    {PublicSessionSchema}
                ],
                "model":SessionModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-16-2023 11:55:48
        `version`: 1.0
        `method_name`: delete
        * @xxx [03-16-2023 11:57:25]: documentation for delete
    '''
    
    return _x.delete_x(
        primary_id=primary_id,
        model=_model,
        primary_column_name=_PRIMARY_COLUMN_NAME,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
        )

