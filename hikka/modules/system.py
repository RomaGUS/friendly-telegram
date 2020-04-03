from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from hikka.services.descriptors import DescriptorService
from hikka.services.models.descriptor import choices
from hikka.services.anime import AnimeService
from hikka.tools.parser import RequestParser
from flask_restful import Resource
from hikka.tools import helpers
from hikka.errors import abort
from hikka import static

class ManagePermissions(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("action", type=str, required=True, choices=("add", "remove"))
        parser.add_argument("account", type=helpers.account, required=True)
        parser.add_argument("scope", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        args = parser.parse_args()

        account = args["account"]

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

        parser = RequestParser()
        parser.add_argument("account", type=helpers.account, required=True)
        args = parser.parse_args()

        account = args["account"]
        result["data"] = account.list_permissions()

        return result

class App(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("descriptors", type=list, default=[], location="json")
        parser.add_argument("static", type=list, default=[], location="json")
        args = parser.parse_args()

        result["data"]["search"] = {}
        data = {}

        for service in args["descriptors"]:
            if service not in choices:
                return abort("general", "service-not-found")

            data[service] = []
            descriptors = DescriptorService.list(service)
            for descriptor in descriptors:
                data[service].append(descriptor.dict())

        result["data"]["search"]["descriptors"] = data

        data = {}
        for service in args["static"]:
            if service not in ["genres", "categories", "states"]:
                return abort("general", "service-not-found")

            data[service] = []
            descriptors = static.static[service]

            for descriptor in descriptors:
                data[service].append(static.dict(service, descriptor))

        result["data"]["search"]["years"] = AnimeService.years()
        result["data"]["search"]["static"] = data

        return result
