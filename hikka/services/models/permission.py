import mongoengine

class Permission(mongoengine.Document):
    scope = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "permissions",
        "indexes": [
            "scope",
            "name",
        ]
    }
