from hikka.decorators import auth_required, permission_required
from hikka.services.descriptors import DescriptorService
from hikka.services.func import update_document
from hikka.tools.parser import RequestParser
from flask.views import MethodView
from hikka.tools import helpers
from hikka.errors import abort
from hikka import utils

class NewDescriptor(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("service", type=helpers.descriptor_service, required=True)
        parser.argument("name", type=str, required=True)
        parser.argument("slug", type=str, required=True)
        parser.argument("description", type=str)
        args = parser.parse()

        check = DescriptorService.get_by_slug(args["service"], args["slug"])
        if check:
            return abort(args["service"], "slug-exists")

        descriptor = DescriptorService.create(
            args["service"],
            args["name"],
            args["slug"],
            args["description"])

        result["data"] = descriptor.dict()
        return result

class UpdateDescriptor(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("service", type=helpers.descriptor_service, required=True)
        parser.argument("slug", type=str, required=True)
        parser.argument("params", type=dict, default={})
        args = parser.parse()

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
