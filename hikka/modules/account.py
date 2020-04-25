from hikka.services.teams import TeamService
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask import request, Blueprint
from hikka.tools import helpers
from hikka.auth import hashpwd

blueprint = Blueprint("account", __name__)

@blueprint.route("/account/password", methods=["POST"])
@auth_required
def password_change():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("password", type=helpers.password, required=True)
    args = parser.parse()

    request.account.password = hashpwd(args["password"])
    request.account.save()

    result["data"] = request.account.dict()
    return result

@blueprint.route("/account/teams", methods=["GET"])
@auth_required
def teams():
    result = {"error": None, "data": []}

    teams = TeamService.member_teams(request.account)
    for team in teams:
        result["data"].append(team.dict(True))

    return result
