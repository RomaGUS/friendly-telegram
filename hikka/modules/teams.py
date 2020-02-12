from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from hikka.services.teams import TeamService
from hikka.services.files import FileService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import request

class NewTeam(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("avatar", type=str, default=None)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        team = TeamService.get_by_slug(args["slug"])
        if team is not None:
            return abort("team", "slug-exists")

        avatar = None
        if args["avatar"] is not None:
            avatar = FileService.get_by_name(args["avatar"])

        team = TeamService.create(args["name"], args["slug"], args["description"])
        PermissionService.add(request.account, f"team-{team.slug}", "admin")
        TeamService.add_member(team, request.account)

        if avatar is not None:
            TeamService.add_avatar(team, avatar)

        result["data"] = {
            "description": team.description,
            "name": team.name,
            "slug": team.slug
        }

        return result
