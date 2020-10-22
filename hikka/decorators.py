from hikka.pony_services import UserService
from hikka.errors import abort
from datetime import datetime
from hikka.auth import Token
from functools import wraps
from flask import request

def auth_required(view_function):
    @wraps(view_function)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authentication")

        valid = Token.validate(token)
        payload = Token.payload(token)

        if valid and payload["action"] == "login":
            account = UserService.get_by_username(payload["meta"])

            if account is None:
                return abort("account", "login-failed")

            if not account.activated:
                return abort("account", "not-activated")

            account.login = datetime.utcnow()
            request.account = account

            return view_function(*args, **kwargs)

        return abort("account", "login-failed")

    return decorator

# ToDo: Implement permissions

# def permission_required(scope, message):
#     def decorator(view_function):
#         @wraps(view_function)
#         def inner_decorator(*args, **kwargs):
#             if not PermissionService.check(request.account, scope, message):
#                 return abort("account", "permission")

#             return view_function(*args, **kwargs)

#         return inner_decorator

#     return decorator
