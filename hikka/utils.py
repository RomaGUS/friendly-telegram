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
