from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from hikka.services.teams import TeamService
from hikka.tools.parser import RequestParser
from hikka.tools import helpers
from hikka.errors import abort
from flask import Blueprint

blueprint = Blueprint("teams", __name__)

@blueprint.route("/teams/new", methods=["POST"])
@auth_required
@permission_required("global", "admin")
def new_team():
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

@blueprint.route("/teams/edit", methods=["POST"])
@auth_required
@permission_required("global", "admin")
def edit_team():
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

@blueprint.route("/teams/get/<string:slug>", methods=["GET"])
@auth_required
def get_team(slug):
    result = {"error": None, "data": {}}

    team = helpers.team(slug)
    result["data"] = team.dict(True)

    return result

@blueprint.route("/teams/member/add", methods=["POST"])
@auth_required
@permission_required("global", "publishing")
def add_member():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("account", type=helpers.account, required=True)
    parser.argument("slug", type=helpers.team, required=True)
    args = parser.parse()

    account = args["account"]
    team = args["slug"]

    TeamService.add_member(team, account)
    result["data"] = team.dict(True)

    return result

@blueprint.route("/teams/member/remove", methods=["POST"])
@auth_required
@permission_required("global", "publishing")
def remove_member():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("account", type=helpers.account, required=True)
    parser.argument("slug", type=helpers.team, required=True)
    args = parser.parse()

    account = args["account"]
    team = args["slug"]

    TeamService.remove_member(team, account)
    PermissionService.remove(account, "global", "publishing")

    result["data"] = team.dict(True)
    return result

@blueprint.route("/teams/list", methods=["GET"])
@auth_required
def list_teams():
    result = {"error": None, "data": []}

    teams = TeamService.list()
    for team in teams:
        result["data"].append(team.dict())

    return result
