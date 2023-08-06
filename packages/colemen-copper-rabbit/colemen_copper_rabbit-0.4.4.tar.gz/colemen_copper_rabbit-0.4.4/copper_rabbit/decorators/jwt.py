

from functools import wraps
from flask import Response
import copper_rabbit.settings as _settings
from copper_rabbit.actions.Token import get_session_auth



def jwt(func):
    # app = _settings.globe.app
    def decorator(*args,**kwargs):
        session = get_session_auth()
        # log(f'model.decorator: {status_code}',"yellow invert")
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result
            # return result
        # print('decorating', f, 'with argument', arg)
        return wrapper
    return decorator
