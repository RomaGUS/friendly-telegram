from hikka.services.statuses import StatusService
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask.views import MethodView
from hikka.tools import helpers
from flask import request
from hikka import static

class Update(MethodView):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("rating", type=int, default=None, choices=range(1, 11))
        parser.argument("subject", type=helpers.content, required=True)
        parser.argument("status", type=int, default=None)
        parser.argument("slug", type=str, default=None)
        args = parser.parse()

        subject = None
        content = static.slug("content", args["subject"])
        if content == "anime":
            subject = helpers.anime(args["slug"])

        status = StatusService.get(subject, request.account, args["subject"])

        fields = ["rating", "status"]
        for field in fields:
            if args[field]:
                status[field] = args[field]

        status.save()
        result["data"] = status.dict()

        return result

class Check(MethodView):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("subject", type=helpers.content, required=True)
        parser.argument("slug", type=str, default=None)
        args = parser.parse()

        subject = None
        content = static.slug("content", args["subject"])
        if content == "anime":
            subject = helpers.anime(args["slug"])

        status = StatusService.get(subject, request.account, args["subject"])
        result["data"] = status.dict()

        return result
