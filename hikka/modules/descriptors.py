from hikka.decorators import auth_required, permission_required
from hikka.services.categories import CategoryService
from hikka.services.func import update_document
from hikka.services.genres import GenreService
from hikka.services.states import StateService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from hikka import utils

def get_service(service):
    if service == "genre":
        return GenreService
    elif service == "category":
        return CategoryService
    elif service == "state":
        return StateService

class NewDescriptor(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("service", type=str, required=True, choices=("genre", "category", "state"))
        parser.add_argument("description", type=str, default=None)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        service = get_service(args["service"])
        check = service.get_by_slug(args["slug"])

        if check is not None:
            return abort(args["service"], "slug-exists")

        descriptor = service.create(args["name"], args["slug"], args["description"])
        result["data"] = {
            "description": descriptor.description,
            "name": descriptor.name,
            "slug": descriptor.slug
        }

        return result

class UpdateDescriptor(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("service", type=str, required=True, choices=("genre", "category", "state"))
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("params", type=dict, default={})

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        service = get_service(args["service"])
        descriptor = service.get_by_slug(args["slug"])

        if descriptor is None:
            return abort(args["service"], "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(args["params"], keys)
        update_document(descriptor, update)

        try:
            descriptor.save()
        except Exception:
            return abort("general", "empty-required")

        result["data"] = {
            "description": descriptor.description,
            "name": descriptor.name,
            "slug": descriptor.slug
        }

        return result
