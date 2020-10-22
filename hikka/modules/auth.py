from hikka.pony_services import UserService
from webargs.flaskparser import use_args
from datetime import datetime, timedelta
from webargs import fields, validate
from hikka.errors import abort
from hikka.auth import Token
from hikka.tools import mail
from flask import Blueprint
import hikka.auth as auth
from pony import orm
import config

blueprint = Blueprint("auth", __name__)

join_args = {
    "username": fields.Str(required=True, validate=validate.Length(min=4, max=32)),
    "password": fields.Str(required=True, validate=validate.Length(min=8)),
    "email": fields.Email(required=True)
}

login_args = {
    "password": fields.Str(required=True, validate=validate.Length(min=8)),
    "email": fields.Email(required=True)
}

activate_args = {
    "token": fields.Str(required=True)
}

forgot_args = {
    "email": fields.Email(required=True)
}

reset_args = {
    "password": fields.Str(required=True, validate=validate.Length(min=8)),
    "token": fields.Str(required=True)
}

@blueprint.route("/join", methods=["POST"])
@use_args(join_args, location="json")
@orm.db_session
def join(args):
    result = {"error": None, "data": {}}

    if UserService.get_by_username(args["username"]):
        return abort("account", "username-exist")

    if UserService.get_by_email(args["email"]):
        return abort("account", "email-exist")

    account = UserService.create(
        args["username"],
        auth.hashpwd(args["password"]),
        args["email"]
    )

    email = mail.Email()
    activation_token = Token.create("activation", account.username)
    email.account_confirmation(account, activation_token)

    result["data"] = {
        "login": int(datetime.timestamp(account.login)),
        "username": account.username
    }

    # Display activation code only in debug mode
    if config.debug:
        result["data"]["code"] = activation_token

    # ToDo: Add permissions here

    return result

@blueprint.route("/login", methods=["POST"])
@use_args(login_args, location="json")
@orm.db_session
def login(args):
    result = {"error": None, "data": {}}

    if not (account := UserService.get_by_email(args["email"])):
        return abort("account", "not-found")

    if not auth.checkpwd(args["password"], account.password):
        return abort("account", "login-failed")

    if not account.activated:
        return abort("account", "not-activated")

    account.login = datetime.utcnow()
    login_token = Token.create("login", account.username)
    data = Token.payload(login_token)

    result["data"] = {
        "token": login_token,
        "expire": data["expire"],
        "username": data["meta"]
    }

    return result

@blueprint.route("/activate", methods=["POST"])
@use_args(activate_args, location="json")
@orm.db_session
def activate(args):
    result = {"error": None, "data": {}}

    if not Token.validate(args["token"]):
        return abort("general", "token-invalid")

    payload = Token.payload(args["token"])

    if not (account := UserService.get_by_username(payload["meta"])):
        return abort("account", "not-found")

    if payload["action"] != "activation":
        return abort("general", "token-invalid-type")

    if account.activated:
        return abort("account", "activated")

    account.activated = True
    result["data"] = {
        "activated": account.activated,
        "username": account.username
    }

    return result

@blueprint.route("/forgot", methods=["POST"])
@use_args(forgot_args, location="json")
@orm.db_session
def forgot(args):
    result = {"error": None, "data": {}}

    if not (account := UserService.get_by_email(args["email"])):
        return abort("account", "not-found")

    if not account.activated:
        return abort("account", "not-activated")

    delta = timedelta(minutes=30)
    if account.reset + delta > datetime.utcnow():
        return abort("account", "reset-cooldown")

    # Use current account password hash to prevent
    # token reusage after password has been changed
    reset_token = Token.create(
        "reset", account.username, delta, account.password
    )

    email = mail.Email()
    email.password_reset(account, reset_token)
    account.reset = datetime.utcnow()

    result["data"] = {
        "success": True
    }

    return result

@blueprint.route("/reset", methods=["POST"])
@use_args(reset_args, location="json")
@orm.db_session
def reset(args):
    result = {"error": None, "data": {}}

    payload = Token.payload(args["token"])
    if "meta" not in payload:
        return abort("general", "token-invalid")

    if payload["action"] != "reset":
        return abort("general", "token-invalid-type")

    account = UserService.get_by_username(payload["meta"])
    if not Token.validate(args["token"], account.password):
        return abort("general", "token-invalid")

    account.password = auth.hashpwd(args["password"])
    result["data"] = {
        "username": account.username,
        "success": True
    }

    return result
