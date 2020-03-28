from hikka.services.permissions import PermissionService
from hikka.services.users import UserService
from hikka.tools.parser import RequestParser
from hikka.tools.mail import Email
from flask_restful import Resource
from hikka.tools import helpers
from hikka.errors import abort
from datetime import datetime
from hikka.auth import Token
import config

class Join(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("email", type=helpers.email, required=True)
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

        account = UserService.get_by_username(args["username"])
        if account:
            return abort("account", "username-exist")

        account_check = UserService.get_by_email(args["email"])
        if account_check:
            return abort("account", "email-exist")

        admin = len(UserService.list()) == 0
        account = UserService.signup(args["username"], args["email"], args["password"])

        # Make first registered user admin
        if admin:
            PermissionService.add(account, "global", "activated")
            PermissionService.add(account, "global", "admin")

        mail = Email()
        activation_token = Token.create("activation", account.username)
        mail.account_confirmation(account.email, activation_token)

        result["data"] = account.dict()

        # Display activation code only in debug mode
        if config.debug:
            result["data"]["code"] = activation_token

        return result

class Login(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("email", type=helpers.email, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

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

        parser = RequestParser()
        parser.add_argument("token", type=str, required=True)
        args = parser.parse_args()

        data = Token.validate(args["token"])
        if not data["valid"]:
            return abort("general", "token-invalid-type")

        account = helpers.account(data["payload"]["meta"])

        if data["payload"]["action"] != "activation":
            return abort("general", "token-invalid-type")

        activated = PermissionService.check(account, "global", "activated")
        if activated:
            return abort("account", "activated")

        PermissionService.add(account, "global", "activated")
        result["data"] = {
            "username": account.username,
            "activated": True
        }

        return result
