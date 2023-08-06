# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The Token action methods

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 03-16-2023 09:53:46
    `name`: Token
    * @xxx [03-16-2023 09:54:06]: documentation for Token
'''


import colemen_utils as _c
import jwt
from sqlalchemy.exc import NoResultFound


import copper_rabbit.settings as _settings
import copper_rabbit.settings.types as _t
import copper_rabbit.schemas.Token as _schemas
from copper_rabbit.support.Result import Result as _result
from copper_rabbit.models.Token import Token as _model
import copper_rabbit.support.actions as _x
from copper_rabbit.support import format_timestamp,current_unix_timestamp
from flask import Flask,request

_PRIMARY_COLUMN_NAME="token_id"
_DEFAULT_PUBLIC_SCHEMA=_schemas.PublicTokenSchema
_DEFAULT_CREATE_SCHEMA=_schemas.CreateTokenSchema
# _DEFAULT_UPDATE_SCHEMA=_schemas.UpdateTokenSchema
def get_session_auth():
    cookie = _c.obj.get_arg(request.cookies,[_settings.control.session_cookie_name],None)
    if cookie is not None:
        print(f"cookie: {cookie}")
    return cookie

def new_from_dict(data,include_model:bool=True)->_t._result_type:
    '''
        Create a new token log
        ----------

        Arguments
        -------------------------
        `data` {dict}
            A dictionary of data for creating a new token.

        Return {Result}
        ----------------------
        A Result instance.

        {
            success:True/False,
            public_response:"Here is the stuff",
            errors:{},
            data:{
                "public":[],
                "model":TokenModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 13:37:43
        `memberOf`: Token
        `version`: 1.0
        `method_name`: new
        * @xxx [03-15-2023 13:44:50]: documentation for new
    '''
    # data['value'] = _c.rand.rand(128)


    return _x.new_x_from_dict(
        data,
        _DEFAULT_CREATE_SCHEMA,
        _DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
    )

# TODO []: get jwt from cookie/header.
# TODO []: get session from token


def get_by_jwt(encoded_token:str):
    result = _result()
    # @Mstep [] attempt to decode the jwt token
    try:
        jwt_result = jwt.decode(encoded_token,_settings.control.token_secret,_settings.control.token_algorithm)

    # @Mstep [IF] if the token is expired
    except jwt.ExpiredSignatureError:
        # @Mstep [] update the Result with the error info
        result.success = False
        result.public_response = "Thats a no go!"
        result.add_error("token","Token has Expired")
        # @Mstep [RETURN] return the Result instance.
        return result

    except jwt.exceptions.ImmatureSignatureError:
        # @Mstep [] update the Result with the error info
        result.success = False
        result.public_response = "Thats a no go!"
        result.add_error("token","Token is not yet valid")
        # @Mstep [RETURN] return the Result instance.
        return result

    except jwt.InvalidSignatureError:
        # @Mstep [] update the Result with the error info
        result.success = False
        result.public_response = "Thats a no go!"
        result.add_error("token","Failed signature validation.")
        # @Mstep [RETURN] return the Result instance.
        return result

    except jwt.DecodeError:
        # @Mstep [] update the Result with the error info
        result.success = False
        result.public_response = "Thats a no go!"
        result.add_error("token","Failed to decode token.")
        # @Mstep [RETURN] return the Result instance.
        return result

    # @Mstep [] attempt to retrieve the token using the jwt value.
    try:
        mdl = _settings.globe.session.query(_model).filter(_model.value==jwt_result['value']).one()
        sch = _DEFAULT_PUBLIC_SCHEMA().dump(mdl)

    # @Mstep [IF] if there is no matching token.
    except NoResultFound:
        # @Mstep [] update the Result with the error info
        result.success = False
        result.public_response = _settings.datas.no_values_found_responses
        result.data = {"schemas":[]}
        # @Mstep [RETURN] return the Result instance.
        return result

    result.success = True
    result.public_response = _settings.datas.successful_get_action_responses
    result.set_key("schemas",[sch])
    result.set_key("models",[mdl])

    return result

def get_by_id(primary_id:str,include_model:bool=False,include_deleted:bool=False)->_t._result_type:
    '''
        Retrieve a token by its id.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded token_id to search for.

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
                    {PublicTokenSchema}
                ],
                "model":TokenModel,
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

def regen_token(primary_id:str):
    result = _x.get_x_by_id(
        primary_id=primary_id,
        primary_column_name=_PRIMARY_COLUMN_NAME,
        model=_model,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
    )
    if result.success is True:
        result.models[0].regen()
        # mdl.regen()

    result = _x.get_x_by_id(
        primary_id=primary_id,
        primary_column_name=_PRIMARY_COLUMN_NAME,
        model=_model,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
    )

    return result

def purge_expired():
    '''Delete all tokens that have an expired timestamp'''
    models = _settings.globe.session.query(_model).filter(_model.expiration>current_unix_timestamp()).all()
    for m in models:
        m.soft_delete()

# def update(data:dict,include_model:bool=False)->_t._result_type:
#     '''
#         update a token.
#         ----------

#         Arguments
#         -------------------------
#         `data` {dict}
#             A dictionary of data to update the token with.

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
#                     {PublicTokenSchema}
#                 ],
#                 "model":TokenModel,
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
        Soft delete a token.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded token_id to search for.

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
                    {PublicTokenSchema}
                ],
                "model":TokenModel,
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
        Undo the Soft deletion of a token.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded token_id to search for.

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
                    {PublicTokenSchema}
                ],
                "model":TokenModel,
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
        Permanently delete a token
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded token_id to search for.

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
                    {PublicTokenSchema}
                ],
                "model":TokenModel,
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

