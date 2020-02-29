from flask import abort as flask_abort
from flask import jsonify
import flask_restful

errors = {
    "account": {
        "email-exist": "Account with this email already exists",
        "username-exist": "Account with this username already exists",
        "activated": "Account already activated",
        "permission": "Account don't have corresponding permission",
        "not-found": "Account not found",
        "not-admin": "Account must be admin",
        "login-failed": "Login failed",
        "not-team-member": "Account is not team member"
    },
    "team": {
        "slug-exists": "Team with this slug already exists",
        "not-found": "Team not found"
    },
    "genre": {
        "slug-exists": "Genre with this slug already exists",
        "not-found": "Genre not found"
    },
    "state": {
        "slug-exists": "State with this slug already exists",
        "not-found": "State not found"
    },
    "category": {
        "slug-exists": "Category with this slug already exists",
        "not-found": "Category not found"
    },
    "release": {
        "slug-exists": "Release with this slug already exists",
        "not-found": "Release not found"
    },
    "file": {
        "not-found": "File not provided",
        "bad-mime": "Unsupported file type",
        "bad-upload-type": "Unsupported upload type",
        "bad-mime-type": "Unsupported mime type",
        "too-big": "File is larger than allowed"
    },
    "image": {
        "not-square": "Image is not square",
        "small-image": "Image is way to slow"
    },
    "episodes": {
        "position-exists": "Episode with this number exists",
        "not-found": "Episode not found"
    },
    "general": {
        "token-invalid-type": "Invalid token type",
        "pagination-error": "Pagination is out of range",
        "missing-field": "Required field is missing",
        "empty-required": "Required field can't be empty",
        "out-of-range": "Number is out of range",
        "method-not-allowed": "Method not allowed",
        "too-many-requests": "Too many requests",
        "not-found": "Not Found"
    }
}

class Api(flask_restful.Api):
    def error_router(self, original_handler, e):
        return original_handler(e)

def get(scope, message):
    error_code = scope.title()
    error_code += "".join([x.title() for x in message.split("-")])

    try:
        error_message = errors[scope][message]
    except Exception:
        error_message = "Unknown error"

    return {
        "error": {
            "message": error_message,
            "code": error_code
        }
    }

def abort(scope, message, status_code=400):
    response = jsonify(get(scope, message))
    response.status_code = status_code
    return response

def reqparse_abort(http_status_code, **kwargs):
    response = abort("general", "missing-field")
    flask_abort(response)
