from hikka.services.permissions import PermissionService
from hikka.services.categories import CategoryService
from hikka.services.func import update_document
from hikka.decorators import auth_required
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import request
from hikka import utils

class NewCategory(Resource):
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

        category = CategoryService.get_by_slug(args["slug"])
        if category is not None:
            return abort("category", "slug-exists")

        category = CategoryService.create(args["name"], args["slug"], args["description"])
        result["data"] = {
            "description": category.description,
            "name": category.name,
            "slug": category.slug
        }

        return result

class UpdateCategory(Resource):
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

        category = CategoryService.get_by_slug(args["slug"])
        if category is None:
            return abort("category", "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(args["params"], keys)
        update_document(category, update)

        try:
            category.save()
        except Exception:
            return abort("general", "empty-required")

        result["data"] = {
            "description": category.description,
            "name": category.name,
            "slug": category.slug
        }

        return result
