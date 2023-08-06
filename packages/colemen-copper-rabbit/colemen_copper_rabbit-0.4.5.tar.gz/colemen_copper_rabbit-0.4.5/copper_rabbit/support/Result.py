# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
import json
from typing import Union
import colemen_utils as c
import inspect


from sqlalchemy.orm.state import InstanceState
from copper_rabbit.settings.globe import base as _base
import copper_rabbit.settings.datas as _datas




@dataclass
class Result:
    success:bool = False
    '''True if the procedure was successful, False otherwise.'''
    data:dict = None
    '''The resulting data response'''
    _public_response:str = None
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
        val = c.obj.get_arg(self.data,__name,None)
        if val is not None:
            if __name in ["schemas"]:
                if len(val) == 1:
                    return c.obj.NestedNamespace(val[0])
            if __name in ["models"]:
                if len(val) == 1:
                    return val[0]
                    # return val[0]
        return val

    @property
    def summary(self):
        '''
            Get this Result's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-16-2023 09:14:46
            `@memberOf`: Result
            `@property`: summary
        '''
        data = {
            "success":self.success,
            "data":self.data,
            "public_response":self.public_response,
            "errors":self.errors,
        }
        return data

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

        # return json.dumps(data)
        return json.dumps(self.summary,default=serialize)

    @property
    def public_response(self):
        '''
            Get this Result's public_response

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-16-2023 10:39:49
            `@memberOf`: Result
            `@property`: public_response
        '''
        value = self._public_response
        return value

    @public_response.setter
    def public_response(self,value:Union[str,list]):
        '''
            Set the Result's public_response property

            If a list is provided, a random element will be selected.

            You can also pass a list name that is defined in copper_rabbit.settings.datas.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-16-2023 10:40:02
            `@memberOf`: Result
            `@property`: public_response
        '''
        if isinstance(value,(str)) is True:
            if hasattr(_datas,value):
                value = getattr(_datas,value)
        if isinstance(value,(list)):
            value = c.rand.option(value)
            
        if isinstance(value,(str)):
            value = c.string.exrex_extrapolation(value)
        self._public_response = value

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
        return json.dumps(self.summary,default=serialize,indent=4)
        # return self.json
        # return f"<Result: {self.success} - {self.public_response}>"

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    # if inspect.isfunction(obj):
    #     return obj.__name__

    # @Mstep [if] if the obj is extends the model base class.
    if isinstance(obj, _base):
        # @Mstep [] convert it to a dictionary.
        model_dict = obj.__dict__
        # @Mstep [] remove the sqlalchemy state key
        model_dict = c.obj.remove_keys(model_dict,['_sa_instance_state'])
        # c.con.log(f"    serialize.modelInstance - model_dict: {model_dict} {type(model_dict).__name__}","magenta")
        # @Mstep [RETURN] return the remaining dict
        return model_dict

    # @Mstep [IF] if the obj is a bytes string.
    if isinstance(obj,(bytes)):
        # @Mstep [return] convert and return the bytes as a string
        return obj.decode("utf-16")
    try:
        d = obj.__dict__
    except AttributeError:
        print(obj)
        print(type(obj).__name__)
        return 'unserializable_value'
        # tval = type(obj)
        # if hasattr(tval,"__name__"):
        #     return type(obj).__name__

        # return obj.__name__
    # @Mstep [RETURN] return the obj __dict__ as a last resort.
    # return obj.__dict__
    return None


# def make_dict_json_safe(d):
#     c.con.log("make_dict_json_safe","info")
#     result = None
#     if isinstance(d,(dict)):
#         result = {}
#         for k,v in d.items():
#             if isinstance(v,_base):
#                 c.con.log(f"    make_dict_json_safe.dict - model class found in data: {v}","magenta")
#                 v = v.__dict__
#             if isinstance(v,InstanceState):
#                 c.con.log(f"    make_dict_json_safe.dict - model class found in data: {v}","magenta")
#                 v = None

#             # if inspect.isclass(v):
#             #     c.con.log(f"    make_dict_json_safe.dict - class found in data: {v}","yellow invert")
#             #     v = v.__dict__
#             if isinstance(v, (dict,list)):
#                 c.con.log("    make_dict_json_safe.dict - nested list/dict found","info")
#                 result[k] = make_dict_json_safe(v)
#             else:
#                 result[k] = v

#     if isinstance(d,(list)):
#         result = []
#         for v in d:
#             if inspect.isclass(v):
#                 c.con.log(f"    make_dict_json_safe.list - class found in data: {v}","info")
#                 v = v.__dict__
#             if isinstance(v, (dict,list)):
#                 result.append(make_dict_json_safe(v))
#             else:
#                 result.append(v)
#     c.con.log(f"    make_dict_json_safe - result: {result}","green")
#     return result