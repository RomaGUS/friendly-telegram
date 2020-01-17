from hikka.services.permissions import PermissionsService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from datetime import datetime
from hikka.auth import Token
from hikka import utils
from hikka import api
import config

class Join(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, default=None)
        parser.add_argument("password", type=str, default=None)
        parser.add_argument("email", type=str, default=None)
        args = parser.parse_args()

        result = {
            "error": utils.errors["account-username-exist"],
            "data": {}
        }

        account = UserService.get_by_username(args["username"])

        if account is None:
            result["error"] = utils.errors["account-email-exist"]
            account_email = UserService.get_by_email(args["email"])

            if account_email is None:
                admin = len(UserService.list()) == 0
                account = UserService.signup(args["username"], args["email"], args["password"])

                if admin:
                    # Make first registered user admin
                    PermissionsService.add(account, "global", "admin")

                result["error"] = None
                result["data"] = {
                    "username": account.username
                }

                if config.debug:
                    # Display activation code only in debug mode
                    result["data"]["code"] = Token.create("activation", account.username)

        return result

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("password", type=str, default=None)
        parser.add_argument("email", type=str, default=None)
        args = parser.parse_args()

        result = {
            "error": utils.errors["account-not-found"],
            "data": {}
        }

        account = UserService.get_by_email(args["email"])

        if account is not None:
            result["error"] = utils.errors["login-failed"]
            login = UserService.login(args["password"], account.password)

            if login:
                UserService.update(account, login=datetime.now)
                token = Token.create("login", account.username)
                data = Token.validate(token)

                result["error"] = None
                result["data"] = {
                    "token": token,
                    "expire": data["payload"]["expire"],
                    "username": data["payload"]["username"]
                }

        return result

class Activate(Resource):
    def get(self, token):
        data = Token.validate(token)
        result = {"error": utils.errors["token-invalid-type"], "data": {}}

        if data["valid"]:
            result["error"] = utils.errors["account-not-found"]
            account = UserService.get_by_username(data["payload"]["username"])

            if account is not None:
                result["error"] = utils.errors["account-activated"]
                activated = PermissionsService.check(account, "accounts", "activated")

                if not activated and data["payload"]["action"] == "activation":
                    PermissionsService.add(account, "accounts", "activated")

                    result["error"] = None
                    result["data"] = {
                        "username": account.username,
                        "activated": True
                    }

        return result


api.add_resource(Join, "/api/join")
api.add_resource(Login, "/api/login")
api.add_resource(Activate, "/api/activate/<string:token>")
