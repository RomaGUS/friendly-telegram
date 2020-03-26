from hikka.services.comments import CommentService
from hikka.services.anime import AnimeService
from hikka.tools.helpers import non_empty_str
from hikka.decorators import auth_required
from datetime import datetime, timedelta
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import request

choices = ("anime")

def get_service(service):
    if service == "anime":
        return AnimeService

class NewComment(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("subject", type=str, required=True, choices=choices)
        parser.add_argument("text", type=non_empty_str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        service = get_service(args["subject"])
        subject = service.get_by_slug(args["slug"])

        comment = CommentService.create(subject, request.account, args["text"])
        result["data"] = comment.dict()

        return result

class UpdateComment(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("counter", type=int, required=True)
        parser.add_argument("params", type=dict, default={})
        args = parser.parse_args()

        params_parser = reqparse.RequestParser()
        params_parser.add_argument("text", type=non_empty_str, required=True, location=("params"))
        params_args = params_parser.parse_args(req=args)

        comment = CommentService.get_by_counter(args["counter"], request.account)
        if comment is None:
            return abort("comments", "not-found")

        if datetime.now() - comment.created > timedelta(minutes=20):
            return abort("comments", "not-editable")

        comment.text = params_args["text"]
        comment.updated = datetime.now()
        comment.save()

        result["data"] = comment.dict()
        return result

class ListComments(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": []}

        parser = reqparse.RequestParser()
        parser.add_argument("subject", type=str, required=True, choices=choices)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("page", type=int, default=0)
        args = parser.parse_args()

        service = get_service(args["subject"])
        subject = service.get_by_slug(args["slug"])
        comments = CommentService.list(subject, args["page"])

        for comment in comments:
            result["data"].append(comment.dict())

        return result
