from hikka.decorators import auth_required, permission_required
from hikka.services.descriptors import DescriptorService
from hikka.services.models.descriptor import choices
from hikka.services.func import update_document
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from hikka import utils

class NewDescriptor(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("service", type=str, required=True, choices=choices)
        parser.add_argument("description", type=str, default=None)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        check = DescriptorService.get_by_slug(args["service"], args["slug"])
        if check is not None:
            return abort(args["service"], "slug-exists")

        descriptor = DescriptorService.create(
            args["service"],
            args["name"],
            args["slug"],
            args["description"])

        result["data"] = descriptor.dict()
        return result

class UpdateDescriptor(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("service", type=str, required=True, choices=choices)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("params", type=dict, default={})
        args = parser.parse_args()

        descriptor = DescriptorService.get_by_slug(args["service"], args["slug"])
        if descriptor is None:
            return abort(args["service"], "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(args["params"], keys)
        update_document(descriptor, update)

        try:
            descriptor.save()
        except Exception:
            return abort("general", "empty-required")

        result["data"] = descriptor.dict()
        return result

class ListDescriptors(Resource):
    def get(self):
        result = {"error": None, "data": []}

        parser = reqparse.RequestParser()
        parser.add_argument("service", type=str, required=True, choices=choices)
        args = parser.parse_args()

        descriptors = DescriptorService.list(args["service"])

        for descriptor in descriptors:
            result["data"].append(descriptor.dict())

        return result
