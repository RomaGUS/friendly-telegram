from hikka.services.comments import CommentService
from hikka.services.anime import AnimeService
from hikka.decorators import auth_required
from flask_restful import Resource
from flask_restful import reqparse
from flask import request

choices = ("anime")

class NewComment(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("subject", type=str, required=True, choices=choices)
        parser.add_argument("text", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        subject = None
        if args["subject"] == "anime":
            subject = AnimeService.get_by_slug(args["slug"])

        comment = CommentService.create(subject, request.account, args["text"])
        result["data"] = comment.dict()

        return result
