from flask import jsonify

errors = {
    "account": {
        "email-exist": "Account with this email already exists",
        "username-exist": "Account with this username already exists",
        "activated": "Account already activated",
        "not-activated": "Account not activated yet",
        "permission": "Account don't have corresponding permission",
        "not-found": "Account not found",
        "not-admin": "Account must be admin",
        "login-failed": "Login failed",
        "not-team-member": "Account is not team member",
        "reset-cooldown": "Password reset cooldown"
    },
    "team": {
        "slug-exists": "Team with this slug already exists",
        "not-found": "Team not found"
    },
    "content": {
        "not-found": "Content type not found"
    },
    "status": {
        "not-found": "Status not found"
    },
    "descriptors": {
        "not-found": "Descriptor service not found"
    },
    "genre": {
        "slug-exists": "Genre with this slug already exists",
        "not-found": "Genre not found"
    },
    "franchise": {
        "slug-exists": "Franchise with this slug already exists",
        "not-found": "Franchise not found"
    },
    "state": {
        "slug-exists": "State with this slug already exists",
        "not-found": "State not found"
    },
    "category": {
        "slug-exists": "Category with this slug already exists",
        "not-found": "Category not found"
    },
    "anime": {
        "slug-exists": "Anime with this slug already exists",
        "not-found": "Anime not found"
    },
    "file": {
        "not-found": "File not provided",
        "bad-mime": "Unsupported file type",
        "bad-upload-type": "Unsupported upload type",
        "bad-mime-type": "Unsupported mime type",
        "too-big": "File is larger than allowed",
        "invalid-size": "Provided file size is invalid",
        "invalid-index": "Invalid index"
    },
    "image": {
        "not-square": "Image is not square",
        "small-image": "Image is way to slow"
    },
    "episode": {
        "position-exists": "Episode with this number exists",
        "not-found": "Episode not found"
    },
    "comment": {
        "not-found": "Comment not found",
        "not-editable": "Comment not editable"
    },
    "general": {
        "token-invalid": "Invalid token",
        "token-invalid-type": "Invalid token type",
        "alias-invalid-type": "Alias must be string",
        "pagination-error": "Pagination is out of range",
        "service-not-found": "Descriptor service not found",
        "not-file-link": "Link doesn't seems to be a file",
        "empty-required": "Required field can't be empty",
        "something-bad": "Something very bad happened",
        "position-range": "Position is out of range",
        "missing-field": "Required field is missing",
        "bad-regex": "Parameter don't match regex",
        "method-not-allowed": "Method not allowed",
        "too-many-requests": "Too many requests",
        "password-length": "Bad password length",
        "file-link-down": "File link is down",
        "invalid-email": "Invalid email",
        "empty-string": "Empty string",
        "bad-request": "Bad request",
        "not-found": "Not found"
    }
}

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
        },
        "data": {}
    }

def abort(scope, message, status_code=422):
    response = jsonify(get(scope, message))
    response.status_code = status_code
    return response
