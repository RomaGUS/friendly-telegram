from hikka.services.statuses import StatusService
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask_restful import Resource
from hikka.tools import helpers
from flask import request
from hikka import static

class Update(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("rating", type=int, default=None, choices=range(1, 11))
        parser.add_argument("subject", type=helpers.content, required=True)
        parser.add_argument("status", type=int, default=None)
        parser.add_argument("slug", type=str, default=None)
        args = parser.parse_args()

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
