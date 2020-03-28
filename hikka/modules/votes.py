from hikka.services.votes import VoteService
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask_restful import Resource
from hikka.tools import helpers
from flask import request

choices = ("anime")

class MakeVote(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("rating", type=int, required=True, choices=range(1, 11))
        parser.add_argument("subject", type=str, required=True, choices=choices)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        subject = None
        if args["subject"] == "anime":
            subject = helpers.anime(args["slug"])
            if type(subject) is Response:
                return subject

        vote = VoteService.submit(subject, request.account, args["rating"])
        result["data"] = vote.dict()

        return result
