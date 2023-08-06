# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The Request action methods

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 03-16-2023 09:53:46
    `name`: Request
    * @xxx [03-16-2023 09:54:06]: documentation for Request
'''



import copper_rabbit.settings.types as _t
import copper_rabbit.schemas.Request as _schemas
from copper_rabbit.models.Request import Request as _model
import copper_rabbit.support.actions as _x


_PRIMARY_COLUMN_NAME="request_id"
_DEFAULT_CREATE_SCHEMA=_schemas.CreateRequestSchema
_DEFAULT_UPDATE_SCHEMA=_schemas.UpdateRequestSchema
_DEFAULT_PUBLIC_SCHEMA=_schemas.PublicRequestSchema



def new_from_dict(data,include_model:bool=True)->_t._result_type:
    '''
        Create a new request log
        ----------

        Arguments
        -------------------------
        `data` {dict}
            A dictionary of data for creating the request log.

        Return {Result}
        ----------------------
        A Result instance.

        {
            success:True/False,
            public_response:"Here is the stuff",
            errors:{},
            data:{
                "public":[],
                "model":RequestModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 13:37:43
        `memberOf`: Request
        `version`: 1.0
        `method_name`: new
        * @xxx [03-15-2023 13:44:50]: documentation for new
    '''
    return _x.new_x_from_dict(
        data,
        _DEFAULT_CREATE_SCHEMA,
        _DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
    )

def get(include_model:bool=True,**kwargs):
    '''
        Retrieve requests by filtering their columns.
        ----------

        Arguments
        -------------------------
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
                    {PublicRequestSchema}
                ],
                "model":RequestModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-16-2023 11:53:40
        `version`: 1.0
        `method_name`: get
        * @TODO []: documentation for get
    '''
    return _x.get_x(
        model=_model,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
        **kwargs
        )

def get_by_id(primary_id:str,include_model:bool=False)->_t._result_type:
    '''
        Retrieve a request by its id.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded request_id to search for.

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
                    {PublicRequestSchema}
                ],
                "model":RequestModel,
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
        )

def update(data:dict,include_model:bool=False)->_t._result_type:
    '''
        update a request.
        ----------

        Arguments
        -------------------------
        `data` {dict}
            A dictionary of data to update the request with.

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
                    {PublicRequestSchema}
                ],
                "model":RequestModel,
            },
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-16-2023 11:55:48
        `version`: 1.0
        `method_name`: update
        * @xxx [03-16-2023 11:57:25]: documentation for update
    '''
    return _x.update_x(
        data,
        update_schema=_DEFAULT_UPDATE_SCHEMA,
        public_schema=_DEFAULT_PUBLIC_SCHEMA,
        include_model=include_model,
        )

def soft_delete(primary_id:str,include_model:bool=False)->_t._result_type:
    '''
        Soft delete a request.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded request_id to search for.

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
                    {PublicRequestSchema}
                ],
                "model":RequestModel,
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
        Undo the Soft deletion of a request.
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded request_id to search for.

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
                    {PublicRequestSchema}
                ],
                "model":RequestModel,
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
        Permanently delete a request
        ----------

        Arguments
        -------------------------
        `primary_id` {str}
            The encoded request_id to search for.

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
                    {PublicRequestSchema}
                ],
                "model":RequestModel,
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

