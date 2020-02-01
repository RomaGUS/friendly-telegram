import hashlib

def blake2b(data: str):
    return hashlib.blake2b(
        str.encode(data),
        digest_size=32
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
