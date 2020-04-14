from hikka.services.teams import TeamService
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask_restful import Resource
from hikka.tools import helpers
from hikka.auth import hashpwd
from flask import request

class PasswordChange(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("password", type=helpers.password, required=True)
        args = parser.parse_args()

        request.account.password = hashpwd(args["password"])
        request.account.save()

        result["data"] = request.account.dict()
        return result

class AccountTeams(Resource):
    @auth_required
    def get(self):
        result = {"error": None, "data": []}

        teams = TeamService.member_teams(request.account)
        for team in teams:
            result["data"].append(team.dict())

        return result
