from functools import wraps

import jwt
from sanic import text

def check_token(request):
    if not request.token:
        return False

    try:
        jwt.decode(
            request.token, request.app.config.SECRET_USER, algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True

def user_protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)
            if is_authenticated:
                json_jwt = jwt.decode(
                    request.token, request.app.config.SECRET_USER, algorithms=["HS256"]
                )
                pk = json_jwt['id']
                response = await f(request, pk, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)
