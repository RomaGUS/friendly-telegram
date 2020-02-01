from hikka.services.permissions import PermissionsService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from datetime import datetime
from hikka.auth import Token
import config

class Join(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("email", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        account = UserService.get_by_username(args["username"])
        if account is not None:
            return abort("account", "username-exist")

        account_check = UserService.get_by_email(args["email"])
        if account_check is not None:
            return abort("account", "email-exist")

        admin = len(UserService.list()) == 0
        account = UserService.signup(args["username"], args["email"], args["password"])

        # Make first registered user admin
        if admin:
            PermissionsService.add(account, "global", "activated")
            PermissionsService.add(account, "global", "admin")

        result["data"] = {
            "username": account.username
        }

        # Display activation code only in debug mode
        if config.debug:
            result["data"]["code"] = Token.create("activation", account.username)

        return result

class Login(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("email", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        account = UserService.get_by_email(args["email"])
        if account is None:
            return abort("account", "not-found")

        login = UserService.login(args["password"], account.password)
        if not login:
            return abort("account", "login-failed")

        UserService.update(account, login=datetime.now)
        token = Token.create("login", account.username)
        data = Token.validate(token)

        result["data"] = {
            "token": token,
            "expire": data["payload"]["expire"],
            "username": data["payload"]["meta"]
        }

        return result

class Activate(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        data = Token.validate(args["token"])
        if not data["valid"]:
            return abort("general", "token-invalid-type")

        account = UserService.get_by_username(data["payload"]["meta"])
        if account is None:
            return abort("account", "not-found")

        if data["payload"]["action"] != "activation":
            return abort("general", "token-invalid-type")

        activated = PermissionsService.check(account, "global", "activated")
        if activated:
            return abort("account", "activated")

        PermissionsService.add(account, "global", "activated")
        result["data"] = {
            "username": account.username,
            "activated": True
        }

        return result
