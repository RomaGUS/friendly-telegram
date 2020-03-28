from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from werkzeug.datastructures import FileStorage
from hikka.services.teams import TeamService
from hikka.tools.parser import RequestParser
from hikka.tools.upload import UploadHelper
from flask_restful import Resource
from hikka.tools import helpers
from hikka.errors import abort
from flask import Response
from flask import request

class NewTeam(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("members", type=list, default=[], location="json")
        parser.add_argument("admins", type=list, default=[], location="json")
        parser.add_argument("avatar", type=FileStorage, location="files")
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        team = TeamService.get_by_slug(args["slug"])
        if team:
            return abort("team", "slug-exists")

        avatar = None
        if args["avatar"]:
            helper = UploadHelper(request.account, args["avatar"], "avatar")
            data = helper.upload_image()

            if type(data) is Response:
                return data

            avatar = data

        team = TeamService.create(args["name"], args["slug"], args["description"])

        if avatar:
            TeamService.update_avatar(team, avatar)

        for username in args["members"]:
            account = helpers.account(username)
            if type(account) is Response:
                return account

            TeamService.add_member(team, account)
            if account.username in args["admins"]:
                PermissionService.add(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class EditTeam(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("slug", type=helpers.team, required=True)
        parser.add_argument("params", type=dict)
        args = parser.parse_args()

        params_parser = RequestParser()
        params_parser.add_argument("description", type=helpers.string, location=("params"))
        params_parser.add_argument("name", type=helpers.string, location=("params"))
        params_args = params_parser.parse_args(req=args)

        team = args["slug"]

        if params_args["description"]:
            team.description = params_args["description"]

        if params_args["name"]:
            team.name = params_args["name"]

        team.save()
        result["data"] = team.dict(True)

        return result

class AddMember(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("account", type=helpers.account, required=True)
        parser.add_argument("slug", type=helpers.team, required=True)
        parser.add_argument("admin", type=bool, default=False)
        args = parser.parse_args()

        account = args["account"]
        team = args["slug"]

        TeamService.add_member(team, account)
        if args["admin"]:
            PermissionService.add(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class RemoveMember(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("account", type=helpers.account, required=True)
        parser.add_argument("slug", type=helpers.team, required=True)
        parser.add_argument("admin", type=bool, default=False)
        args = parser.parse_args()

        account = args["account"]
        team = args["slug"]

        TeamService.remove_member(team, account)
        PermissionService.remove(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class GetTeam(Resource):
    @auth_required
    def get(self, slug):
        result = {"error": None, "data": {}}

        team = helpers.team(slug)
        if type(team) is Response:
            return team

        result["data"] = team.dict(True)

        return result

class ListTeams(Resource):
    @auth_required
    def get(self):
        result = {"error": None, "data": []}

        teams = TeamService.list()
        for team in teams:
            result["data"].append(team.dict())

        return result
