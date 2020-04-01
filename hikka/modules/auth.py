from hikka.services.permissions import PermissionService
from hikka.services.users import UserService
from hikka.tools.parser import RequestParser
from datetime import datetime, timedelta
from hikka.auth import Token, hashpwd
from hikka.tools.mail import Email
from flask_restful import Resource
from hikka.tools import helpers
from hikka.errors import abort
import config

class Join(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("password", type=helpers.password, required=True)
        parser.add_argument("email", type=helpers.email, required=True)
        parser.add_argument("username", type=str, required=True)
        args = parser.parse_args()

        account = UserService.get_by_username(args["username"])
        if account:
            return abort("account", "username-exist")

        account_check = UserService.get_by_email(args["email"])
        if account_check:
            return abort("account", "email-exist")

        admin = len(UserService.list()) == 0
        account = UserService.signup(args["username"], args["email"], args["password"])

        mail = Email()
        activation_token = Token.create("activation", account.username)
        mail.account_confirmation(account.email, activation_token)

        result["data"] = account.dict()

        # Display activation code only in debug mode
        if config.debug:
            result["data"]["code"] = activation_token

        # Make first registered user admin
        if admin:
            PermissionService.add(account, "global", "activated")
            PermissionService.add(account, "global", "admin")

        return result

class Login(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("password", type=helpers.password, required=True)
        parser.add_argument("email", type=helpers.email, required=True)
        args = parser.parse_args()

        account = UserService.get_by_email(args["email"])
        if account is None:
            return abort("account", "not-found")

        login = UserService.login(args["password"], account.password)
        if not login:
            return abort("account", "login-failed")

        activated = PermissionService.check(account, "global", "activated")
        if not activated:
            return abort("account", "not-activated")

        UserService.update(account, login=datetime.now)
        login_token = Token.create("login", account.username)
        data = Token.payload(login_token)

        result["data"] = {
            "token": login_token,
            "expire": data["expire"],
            "username": data["meta"]
        }

        return result

class Activate(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("token", type=str, required=True)
        args = parser.parse_args()

        if not Token.validate(args["token"]):
            return abort("general", "token-invalid")

        payload = Token.payload(args["token"])
        account = helpers.account(payload["meta"])

        if payload["action"] != "activation":
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

class RequestReset(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("email", type=helpers.email, required=True)
        args = parser.parse_args()

        account = UserService.get_by_email(args["email"])
        if account is None:
            return abort("account", "not-found")

        delta = timedelta(minutes=30)
        if account.reset + delta > datetime.now():
            return abort("account", "reset-cooldown")

        mail = Email()
        reset_token = Token.create("reset", account.username, delta, account.password)

        mail.password_reset(account.email, reset_token)
        account.reset = datetime.now()
        account.save()

        result["data"] = {
            "success": True
        }

        return result

class PasswordReset(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("password", type=helpers.password, required=True)
        parser.add_argument("token", type=str, required=True)
        args = parser.parse_args()

        payload = Token.payload(args["token"])
        if "meta" not in payload:
            return abort("general", "token-invalid")

        account = helpers.account(payload["meta"])
        if not Token.validate(args["token"], account.password):
            return abort("general", "token-invalid")

        if payload["action"] != "reset":
            return abort("general", "token-invalid-type")

        account.password = hashpwd(args["password"])
        account.save()

        result["data"] = {
            "username": account.username,
            "success": True
        }

        return result
