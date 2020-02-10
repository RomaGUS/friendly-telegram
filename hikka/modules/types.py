from hikka.services.permissions import PermissionService
from hikka.services.types import ReleaseTypesService
from hikka.services.func import update_document
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from hikka import utils

class NewReleaseType(Resource):
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

        if not PermissionService.check(account, "global", "admin"):
            return abort("account", "permission")

        rtype = ReleaseTypesService.get_by_slug(args["slug"])
        if rtype is not None:
            return abort("type", "slug-exists")

        rtype = ReleaseTypesService.create(args["name"], args["slug"], args["description"])
        result["data"] = {
            "description": rtype.description,
            "name": rtype.name,
            "slug": rtype.slug
        }

        return result

class UpdateReleaseType(Resource):
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
        params_parser.add_argument("description", type=str, location=("params",))
        params_parser.add_argument("name", type=str, location=("params",))
        params_parser.add_argument("slug", type=str, location=("params",))
        params_args = params_parser.parse_args(req=args)

        account = UserService.auth(args["auth"])
        if account is None:
            return abort("account", "not-found")

        if not PermissionService.check(account, "global", "admin"):
            return abort("account", "permission")

        rtype = ReleaseTypesService.get_by_slug(args["slug"])
        if rtype is None:
            return abort("type", "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(params_args, keys)
        update_document(rtype, update)
        rtype.save()

        result["data"] = {
            "description": rtype.description,
            "name": rtype.name,
            "slug": rtype.slug
        }

        return result
