static = {
    "statuses": {1: "active", 2: "finished", 3: "hold", 4: "dropped", 5: "planned"},
    "categories": {1: "tv", 2: "movie", 3: "special", 4: "ova", 5: "ona"},
    "states": {1: "ongoing", 2: "released", 3: "announced"},
    "descriptors": {1: "franchise"},
    "content": {1: "anime"},
    "genres": {
        1: "action", 2: "adventure", 3: "cars", 4: "comedy", 5: "dementia", 6: "demons",
        7: "drama", 8: "ecchi", 9: "fantasy", 10: "game", 11: "harem", 12: "hentai",
        13: "historical", 14: "horror", 15: "josei", 16: "kids", 17: "magic", 18: "martial_arts",
        19: "mecha", 20: "military", 21: "music", 22: "mystery", 23: "parody", 24: "police",
        25: "psychological", 26: "romance", 27: "samurai", 28: "school", 29: "sci_fi",
        30: "seinen", 31: "shoujo", 32: "shoujo_ai", 33: "shounen", 34: "shounen_ai",
        35: "slice_of_life", 36: "space", 37: "sports", 38: "superpower", 39: "supernatural",
        40: "thriller", 41: "vampire", 42: "yaoi", 43: "yuri"
    }
}

def key(service, slug):
    if service in static:
        for key in static[service]:
            if (static[service][key] == slug):
                return key

    return None

def slug(service, key):
    return static[service][key]
