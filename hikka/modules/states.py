from hikka.services.permissions import PermissionsService
from hikka.services.states import StatesService
from hikka.services.func import update_document
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from hikka import utils

class NewState(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, default=None)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("auth", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        account = UserService.auth(args["auth"])
        if account is None:
            return abort("account", "not-found")

        if not PermissionsService.check(account, "global", "admin"):
            return abort("account", "permission")

        state_check = StatesService.get_by_slug(args["slug"])
        if state_check is not None:
            return abort("state", "slug-exists")

        state = StatesService.create(args["name"], args["slug"], args["description"])
        result["data"] = {
            "description": state.description,
            "name": state.name,
            "slug": state.slug
        }

        return result

class UpdateState(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("auth", type=str, required=True)
        parser.add_argument("params", type=dict, default={})

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        params_parser = reqparse.RequestParser()
        params_parser.add_argument("name", type=str, location=("params",))
        params_parser.add_argument("slug", type=str, location=("params",))
        params_parser.add_argument("description", type=str, location=("params",))
        params_args = params_parser.parse_args(req=args)

        account = UserService.auth(args["auth"])
        if account is None:
            return abort("account", "not-found")

        if not PermissionsService.check(account, "global", "admin"):
            return abort("account", "permission")

        state = StatesService.get_by_slug(args["slug"])
        if state is None:
            return abort("state", "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(params_args, keys)
        update_document(state, update)
        state.save()

        result["data"] = {
            "description": state.description,
            "name": state.name,
            "slug": state.slug
        }

        return result
