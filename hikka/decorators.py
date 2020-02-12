from hikka.services.permissions import PermissionService
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

def permission_required(scope, message):
    def decorator(view_function):
        @wraps(view_function)
        def inner_decorator(*args, **kwargs):
            if not PermissionService.check(request.account, scope, message):
                return abort("account", "permission")

            return view_function(*args, **kwargs)

        return inner_decorator

    return decorator
