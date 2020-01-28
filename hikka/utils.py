import hashlib
import os

def sha256(password: str):
    encoded_password = str.encode(password)
    return hashlib.sha256(encoded_password).digest()

def pebble():
    """
    Generate random 32 characters string
    """
    return os.urandom(16).hex()

def check_fields(fields: list, data: dict):
    """
    Check if given dict `data` contain given list of keys from list `fields`.
    """
    for field in fields:
        if field not in data:
            return f"{field.title()} is not set"

    return None

def filter_dict(data, keys):
    """
    Filter dict by given keys
    """
    result = {}
    for key in keys:
        if key in data:
            result[key] = data[key]

    return result


errors = {
    "account-email-exist": "Account with this email already exists",
    "account-username-exist": "Account with this username already exists",
    "account-activated": "Account already activated",
    "account-permission": "Account don't have corresponding permission",
    "login-failed": "Login failed",
    "account-not-found": "User not found",
    "user-activated": "User already activated",
    "account-not-admin": "User must be admin",
    "token-invalid-type": "Invalid token type",
    "pagination-error": "Pagination is out of range",
    "team-slug-exists": "Team with this slug already exists",
    "genre-slug-exists": "Genre with this slug already exists",
    "genre-not-found": "Genre not found"
}
