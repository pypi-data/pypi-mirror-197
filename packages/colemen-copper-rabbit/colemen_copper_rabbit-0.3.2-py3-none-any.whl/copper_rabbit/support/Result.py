# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
import json
import colemen_utils as c
# from flask import Flask,redirect,url_for,request,Blueprint
# from apricity_labs import main as _main
# import apricity.objects.Log as _log


@dataclass
class Result:
    success:bool = False
    '''True if the procedure was successful, False otherwise.'''
    data:dict = None
    '''The resulting data response'''
    public_response:str = None
    '''The response that can be presented to a user.'''
    errors:dict = None
    '''A dictionary of errors field:"error message"'''

    def __init__(self):
        # self.main = _main
        # self.app = _main.app
        self.settings = {}
        self._data = {
            "success":False,
            "data":None,
            "public_response":None,
        }
        self.data = {}
        self.errors = {}

    def __getattr__(self,__name):
        return c.obj.get_arg(self.data,__name,None)


    @property
    def json(self):
        '''
            Get this Result as a JSON string.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 11-21-2022 16:09:59
            `@memberOf`: __init__
            `@property`: json
        '''
        data = {
            "success":self.success,
            "data":self.data,
            "public_response":self.public_response,
        }
        return json.dumps(data)

    def add_error(self,key,value=None):
        if isinstance(key,(dict)):
            # self.errors = {**self.errors,**key}
            for k,v in key.items():
                if isinstance(v,(list)) and len(v) == 1:
                    v = v[0]
                self.errors[k] = v
        else:
            self.errors[key] = value


    def set_key(self,key,value):
        '''
            Set a key value pair on this result's data dictionary
            ----------

            Arguments
            -------------------------
            `key` {str}
                The key to set
            `value` {any}
                The value to set.


            Return
            ----------------------
            returns nothing.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-06-2022 09:31:25
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: set_key
            * @xxx [12-06-2022 09:32:17]: documentation for set_key
        '''
        d = self.data
        if d is None:
            d = {}
        d[key] = value
        self.data = d

    def get_key(self,key,default=None,value_type=None):
        '''
            Get a key's value from this result.
            ----------

            Arguments
            -------------------------
            `key` {str}
                The key to search for.

            [`default`=None] {any}
                The default value to return if the key cannot be found.

            [`value_type`=None] {type,tuple}
                A python type or tuple of types that the value must match.

            Return {any}
            ----------------------
            The key's value if it is found, the default value otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-06-2022 09:32:43
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_key
            * @xxx [12-06-2022 09:34:32]: documentation for get_key
        '''
        d = self.data
        if isinstance(d,(dict)) is False:
            return default

        result = c.obj.get_arg(d,key,default,value_type)
        return result


    def __repr__(self) -> str:
        return self.json
        return f"<Result: {self.success} - {self.public_response}>"