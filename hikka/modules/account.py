from hikka.decorators import auth_required
from webargs.flaskparser import use_args
from webargs import fields, validate
from flask import request, Blueprint
from hikka.auth import hashpwd
from pony import orm

blueprint = Blueprint("account", __name__)

password_args = {
    "password": fields.Str(required=True, validate=validate.Length(min=8))
}

@blueprint.route("/password", methods=["POST"])
@use_args(password_args, location="json")
@orm.db_session
@auth_required
def password_change(args):
    result = {"error": None, "data": {}}

    request.account.password = hashpwd(args["password"])

    result["data"] = {
        "username": request.account.username
    }

    return result

@blueprint.route("/me", methods=["GET"])
@orm.db_session
@auth_required
def account():
    result = {"error": None, "data": []}

    result["data"] = {
        "username": request.account.username
    }

    return result
