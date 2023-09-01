from functools import wraps
from sanic.response import json 
from utils.settings import API_CODES


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if request.ctx.is_authenticated:
                return await f(request, *args, **kwargs)
            return json({"response": API_CODES[1002]}, status=401)
        return decorated_function
    return decorator