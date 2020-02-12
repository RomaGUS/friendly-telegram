from hikka.services.permissions import PermissionService
from hikka.services.states import StateService
from hikka.services.func import update_document
from hikka.decorators import auth_required
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import request
from hikka import utils

class NewState(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, default=None)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        if not PermissionService.check(request.account, "global", "admin"):
            return abort("account", "permission")

        state_check = StateService.get_by_slug(args["slug"])
        if state_check is not None:
            return abort("state", "slug-exists")

        state = StateService.create(args["name"], args["slug"], args["description"])
        result["data"] = {
            "description": state.description,
            "name": state.name,
            "slug": state.slug
        }

        return result

class UpdateState(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("params", type=dict, default={})

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        if not PermissionService.check(request.account, "global", "admin"):
            return abort("account", "permission")

        state = StateService.get_by_slug(args["slug"])
        if state is None:
            return abort("state", "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(args["params"], keys)
        update_document(state, update)

        try:
            state.save()
        except Exception:
            return abort("general", "empty-required")

        result["data"] = {
            "description": state.description,
            "name": state.name,
            "slug": state.slug
        }

        return result
