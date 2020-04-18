from hikka.services.teams import TeamService
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask.views import MethodView
from hikka.tools import helpers
from hikka.auth import hashpwd
from flask import request

class PasswordChange(MethodView):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("password", type=helpers.password, required=True)
        args = parser.parse()

        request.account.password = hashpwd(args["password"])
        request.account.save()

        result["data"] = request.account.dict()
        return result

class AccountTeams(MethodView):
    @auth_required
    def get(self):
        result = {"error": None, "data": []}

        teams = TeamService.member_teams(request.account)
        for team in teams:
            result["data"].append(team.dict(True))

        return result
