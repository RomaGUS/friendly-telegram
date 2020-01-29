from hikka.services.permissions import PermissionsService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka import utils

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
                result["error"] = utils.errors["team-slug-exists"]
                team = TeamService.get_by_slug(args["slug"])

                if team is None:
                    team = TeamService.create(args["name"], args["slug"], args["description"])
                    PermissionsService.add(account, f"team-{team.slug}", "admin")
                    TeamService.add_member(team, account)

                    result["error"] = None
                    result["data"] = {
                        "description": team.description,
                        "name": team.name,
                        "slug": team.slug
                    }

        return result
