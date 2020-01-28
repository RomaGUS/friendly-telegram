import mongoengine

class Genre(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(default=None)
    slug = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "genres",
        "indexes": [
            "name",
            "slug",
        ]
    }
