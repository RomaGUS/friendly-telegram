static = {
    "genres": {
        1: ["action", "Екшн"],
        2: ["adventure", "Пригоди"],
        3: ["cars", "Автівки"],
        4: ["comedy", "Комедія"],
        5: ["dementia", "Деменція"],
        6: ["demons", "Демони"],
        7: ["drama", "Драма"],
        8: ["ecchi", "Еччі"],
        9: ["fantasy", "Фентезі"],
        10: ["game", "Ігри"],
        11: ["harem", "Гарем"],
        12: ["hentai", "Хентий"],
        13: ["historical", "Історичне"],
        14: ["horror", "Хоррор"],
        15: ["josei", "Дзьосей"],
        16: ["kids", "Діти"],
        17: ["magic", "Магія"],
        18: ["martial_arts", "Бойові мистецтва"],
        19: ["mecha", "Мехи"],
        20: ["military", "Військове"],
        21: ["music", "Музика"],
        22: ["mystery", "Таємниця"],
        23: ["parody", "Пародія"],
        24: ["police", "Поліцій"],
        25: ["psychological", "Психологічне"],
        26: ["romance", "Романтика"],
        27: ["samurai", "Самураї"],
        28: ["school", "Школа"],
        29: ["sci_fi", "Наукова фантастика"],
        30: ["seinen", "Сейнен"],
        31: ["shoujo", "Сьодзьо"],
        32: ["shoujo_ai", "Сьодзьо-ай"],
        33: ["shounen", "Сьонен"],
        34: ["shounen_ai", "Сьонен-ай"],
        35: ["slice_of_life", "Буденність"],
        36: ["space", "Космос"],
        37: ["sports", "Спорт"],
        38: ["superpower", "Суперсила"],
        39: ["supernatural", "Надприроднє"],
        40: ["thriller", "Триллер"],
        41: ["vampire", "Вампіри"],
        42: ["yaoi", "Яой"],
        43: ["yuri", "Юрі"]
    },
    "categories": {
        1: ["tv", "TV Серіал"],
        2: ["movie", "Фільм"],
        3: ["special", "Спешл"],
        4: ["ova", "OVA"],
        5: ["ona", "ONA"]
    },
    "states": {
        1: ["ongoing", "Онгоїнг"],
        2: ["released", "Завершений"],
        3: ["аnnounced", "Анонс"]
    }
}


def get_key(service, value):
    if service in static:
        for key in static[service]:
            if (static[service][key][0] == value):
                return key

    return None

def dict(service, key):
    return {
        "slug": static[service][key][0],
        "name": static[service][key][1]
    }
