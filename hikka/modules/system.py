from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort

class ManagePermissions(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("action", type=str, required=True, choices=("add", "remove"))
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("scope", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        args = parser.parse_args()

        account = UserService.get_by_username(args["username"])
        if account is None:
            return abort("account", "not-found")

        if args["action"] == "add":
            PermissionService.add(account, args["scope"], args["name"])

        elif args["action"] == "remove":
            PermissionService.remove(account, args["scope"], args["name"])

        result["data"] = account.list_permissions()
        return result

class UserPermissions(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        args = parser.parse_args()

        account = UserService.get_by_username(args["username"])
        if account is None:
            return abort("account", "not-found")

        result["data"] = account.list_permissions()
        return result
