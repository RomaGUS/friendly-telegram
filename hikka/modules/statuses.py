from hikka.services.statuses import StatusService
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask import request, Blueprint
from hikka.tools import helpers
from datetime import datetime
from hikka import static

blueprint = Blueprint("statuses", __name__)

@blueprint.route("/status", methods=["POST"])
@auth_required
def update_status():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("rating", type=int, default=None, choices=range(1, 11))
    parser.argument("position", type=helpers.position, default=None)
    parser.argument("subject", type=helpers.content, required=True)
    parser.argument("status", type=helpers.status, default=None)
    parser.argument("time", type=int, default=None)
    parser.argument("slug", type=str, default=None)
    args = parser.parse()

    subject = None
    content = static.slug("content", args["subject"])
    if content == "anime":
        subject = helpers.anime(args["slug"])

    status = StatusService.get(subject, request.account, args["subject"])

    fields = ["rating", "status", "position", "time"]
    for field in fields:
        if args[field]:
            # Record rewatch
            if field == "position":
                if status[field] and args[field] < status[field]:
                    status["rewatch"] += 1

            status[field] = args[field]

    status.updated = datetime.now()
    status.save()

    result["data"] = status.dict()
    return result

@blueprint.route("/status/check", methods=["POST"])
@auth_required
def check_status():
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

@blueprint.route("/status/list", methods=["POST"])
@auth_required
def list_status():
    result = {"error": None, "data": []}

    parser = RequestParser()
    parser.argument("subject", type=helpers.content, required=True)
    parser.argument("page", type=int, default=0)
    args = parser.parse()

    statuses = StatusService.get_by_account(request.account, args["subject"])
    for status in statuses:
        result["data"].append(status.dict())

    return result
