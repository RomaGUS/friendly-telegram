import hashlib

def blake2b(data: str, size=32, key=""):
    return hashlib.blake2b(
        str.encode(data),
        key=str.encode(key),
        digest_size=size
    ).digest()

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
