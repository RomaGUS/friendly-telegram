from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from werkzeug.datastructures import FileStorage
from hikka.services.teams import TeamService
from hikka.upload import UploadHelper
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import Response
from flask import request

class NewTeam(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("avatar", type=FileStorage, location="files")
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        team = TeamService.get_by_slug(args["slug"])
        if team is not None:
            return abort("team", "slug-exists")

        avatar = None
        if args["avatar"] is not None:
            helper = UploadHelper(request.account, args["avatar"], "avatar")
            data = helper.upload_image()

            if type(data) is Response:
                return data

            avatar = data

        team = TeamService.create(args["name"], args["slug"], args["description"])
        PermissionService.add(request.account, f"team-{team.slug}", "admin")
        TeamService.add_member(team, request.account)

        if avatar is not None:
            TeamService.update_avatar(team, avatar)

        result["data"] = team.dict()

        return result
