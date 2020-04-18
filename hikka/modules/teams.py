from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from werkzeug.datastructures import FileStorage
from hikka.services.files import FileService
from hikka.services.teams import TeamService
from hikka.tools.parser import RequestParser
from hikka.tools.upload import UploadHelper
from flask.views import MethodView
from hikka.tools import helpers
from hikka.errors import abort
from flask import request

class NewTeam(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("members", type=list, default=[], location="json")
        parser.argument("admins", type=list, default=[], location="json")
        parser.argument("description", type=str, required=True)
        parser.argument("name", type=str, required=True)
        parser.argument("slug", type=str, required=True)
        args = parser.parse()

        team = TeamService.get_by_slug(args["slug"])
        if team:
            return abort("team", "slug-exists")

        team = TeamService.create(args["name"], args["slug"], args["description"])

        for username in args["members"]:
            account = helpers.account(username)
            TeamService.add_member(team, account)
            if account.username in args["admins"]:
                PermissionService.add(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class EditTeam(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("slug", type=helpers.team, required=True)
        parser.argument("params", type=dict)
        args = parser.parse()

        params_parser = RequestParser()
        params_parser.argument("description", type=helpers.string, location=("params"))
        params_parser.argument("name", type=helpers.string, location=("params"))
        params_args = params_parser.parse(req=args)

        team = args["slug"]

        if params_args["description"]:
            team.description = params_args["description"]

        if params_args["name"]:
            team.name = params_args["name"]

        team.save()
        result["data"] = team.dict(True)

        return result

class TeamUpload(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def put(self):
        result = {"error": None, "data": []}
        choices = ("avatar")

        parser = RequestParser()
        parser.argument("file", type=FileStorage, location="files")
        parser.argument("slug", type=helpers.team, required=True)
        parser.argument("type", type=str, choices=choices)
        args = parser.parse()

        team = args["slug"]

        if args["file"]:
            helper = UploadHelper(request.account, args["file"], args["type"])
            data = helper.upload_image()

            if team[args["type"]]:
                FileService.destroy(team[args["type"]])

            team[args["type"]] = data
            team.save()

        result["data"] = team.dict()
        return result

class AddMember(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("account", type=helpers.account, required=True)
        parser.argument("slug", type=helpers.team, required=True)
        parser.argument("admin", type=bool, default=False)
        args = parser.parse()

        account = args["account"]
        team = args["slug"]

        TeamService.add_member(team, account)
        if args["admin"]:
            PermissionService.add(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class RemoveMember(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("account", type=helpers.account, required=True)
        parser.argument("slug", type=helpers.team, required=True)
        parser.argument("admin", type=bool, default=False)
        args = parser.parse()

        account = args["account"]
        team = args["slug"]

        TeamService.remove_member(team, account)
        PermissionService.remove(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class GetTeam(MethodView):
    @auth_required
    def get(self, slug):
        result = {"error": None, "data": {}}

        team = helpers.team(slug)
        result["data"] = team.dict(True)

        return result

class ListTeams(MethodView):
    @auth_required
    def get(self):
        result = {"error": None, "data": []}

        teams = TeamService.list()
        for team in teams:
            result["data"].append(team.dict())

        return result
