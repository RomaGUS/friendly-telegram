from flask import Blueprint
from hikka import errors

blueprint = Blueprint("errors", __name__)

@blueprint.errorhandler(400)
def error400(error):
    return errors.abort("general", "bad-request", 400)

@blueprint.errorhandler(422)
def error422(error):
    return errors.abort("general", "missing-field", 422)

@blueprint.errorhandler(404)
def error404(error):
    return errors.abort("general", "not-found", 404)

@blueprint.errorhandler(405)
def error405(error):
    return errors.abort("general", "method-not-allowed", 405)

@blueprint.errorhandler(429)
def error429(error):
    return errors.abort("general", "too-many-requests", 429)

@blueprint.errorhandler(500)
def error500(error):
    return errors.abort("general", "something-bad", 500)
