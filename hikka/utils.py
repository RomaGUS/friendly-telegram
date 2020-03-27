from jikanpy import Jikan
import hashlib
import secrets
import re

def blake2b(data: str, size=32, key=""):
    """Hash wrapper for blake2b"""
    return hashlib.blake2b(
        str.encode(data),
        key=str.encode(key),
        digest_size=size
    ).digest()

def check_fields(fields: list, data: dict):
    """Check if given dict :data contain given list of keys from list :fields"""
    for field in fields:
        if field not in data:
            return f"{field.title()} is not set"

    return None

def filter_dict(data, keys):
    """Filter dict :data by given :keys"""
    result = {}
    for key in keys:
        if key in data:
            result[key] = data[key]

    return result

def create_slug(text):
    """Create human readable URL based on :text"""
    text = text.strip()
    text = " ".join(text.split())
    text = text.lower()

    replace = {
        "а": "a", "б": "b", "в": "v",
        "г": "g", "ґ": "g", "д": "d",
        "е": "e", "є": "ye", "ё": "e",
        "ж": "j", "з": "z", "и": "i",
        "і": "i", "ї": "i", "й": "y",
        "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p",
        "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "h",
        "ц": "c", "ч": "ch", "ш": "sh",
        "щ": "shch", "ы": "y", "э": "e",
        "ю": "yu", "я": "ya", "ъ": "",
        "ь": ""
    }

    buffer = []
    i, n = 0, len(text)

    while i < n:
        match = False
        for s, r in replace.items():
            if text[i:len(s) + i] == s:
                buffer.append(r)
                i = i + len(s)
                match = True
                break

        if not match:
            buffer.append(text[i])
            i = i + 1

    text = "".join(buffer)
    text = text.replace(" ", "-")
    text = text.strip("-")

    text = re.sub(r"[^\w-]", r"", text)
    text = re.sub(r"{(.)\1+}", r"$1", text)
    text = re.sub(r"-+", r"-", text)
    text = "{}-{}".format(text, secrets.token_hex(4))

    return text

def search_query(query):
    """Process search query"""
    return re.sub(r"[^\w]", r"", query.lower())

def create_search(*args):
    """Create search string based on :args"""
    result = []
    for item in args:
        if type(item) is str:
            result.append(search_query(item))
        elif type(item) is list:
            for alias in item:
                result.append(search_query(alias))

    return " ".join(result)

def rating(code):
    try:
        jikan = Jikan()
        data = jikan.anime(code)
        return data["score"]
    except Exception:
        return 0
