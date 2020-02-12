from hikka.services.users import UserService
from hikka.errors import abort
from functools import wraps
from flask import request

def auth_required(view_function):
    @wraps(view_function)
    def decorator(*args, **kwargs):
        account = UserService.auth(request.headers.get("Authentication"))
        if account is None:
            return abort("account", "login-failed")

        request.account = account
        return view_function(*args, **kwargs)

    return decorator
