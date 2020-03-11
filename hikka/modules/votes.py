from hikka.services.anime import AnimeService
from hikka.services.votes import VoteService
from hikka.decorators import auth_required
from flask_restful import Resource
from flask_restful import reqparse
from flask import request

choices = ("anime")

class MakeVote(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("rating", type=int, required=True, choices=range(1, 11))
        parser.add_argument("subject", type=str, required=True, choices=choices)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        subject = None
        if args["subject"] == "anime":
            subject = AnimeService.get_by_slug(args["slug"])

        vote = VoteService.submit(subject, request.account, args["rating"])
        result["data"] = vote.dict()

        return result
