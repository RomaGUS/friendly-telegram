import mongoengine

class ReleaseType(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(default=None)
    slug = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "types",
        "indexes": [
            "name",
            "slug",
        ]
    }
