from hikka.services.permissions import PermissionsService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka import utils
from hikka import api

class NewTeam(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, default=None, required=True)
        parser.add_argument("name", type=str, default=None, required=True)
        parser.add_argument("slug", type=str, default=None, required=True)
        parser.add_argument("auth", type=str, default=None, required=True)
        args = parser.parse_args()

        result = {
            "error": utils.errors["account-not-found"],
            "data": {}
        }

        account = UserService.auth(args["auth"])

        if account is not None:
            result["error"] = utils.errors["account-permission"]

            if PermissionsService.check(account, "global", "teams"):
                # ToDo: Add check if slug is exists
                team = TeamService.create(args["name"], args["description"], args["slug"])

        return result


api.add_resource(NewTeam, "/api/teams/new")
