from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from hikka.services.anime import AnimeService
from hikka.tools.parser import RequestParser
from flask.views import MethodView
from hikka.tools import helpers
from flask import Blueprint

blueprint = Blueprint("system", __name__)

@blueprint.route("/system/permissions/manage", methods=["POST"])
@auth_required
@permission_required("global", "admin")
def manage_permissions():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("action", type=str, required=True, choices=("add", "remove"))
    parser.argument("account", type=helpers.account, required=True)
    parser.argument("scope", type=str, required=True)
    parser.argument("name", type=str, required=True)
    args = parser.parse()

    account = args["account"]

    if args["action"] == "add":
        PermissionService.add(account, args["scope"], args["name"])

    elif args["action"] == "remove":
        PermissionService.remove(account, args["scope"], args["name"])

    result["data"] = account.list_permissions()

    return result

@blueprint.route("/system/permissions/user", methods=["POST"])
@auth_required
@permission_required("global", "admin")
def user_permissions():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("account", type=helpers.account, required=True)
    args = parser.parse()

    account = args["account"]
    result["data"] = account.list_permissions()

    return result

@blueprint.route("/system/static", methods=["GET"])
@auth_required
def static_data():
    result = {"error": None, "data": {}}
    result["data"]["years"] = AnimeService.years()
    return result
