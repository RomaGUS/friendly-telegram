import mongoengine

class Team(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    slug = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    members = mongoengine.ListField(mongoengine.ReferenceField("User"))
    hidden = mongoengine.BooleanField(required=True, default=False)
    avatar = mongoengine.ReferenceField("File")

    meta = {
        "alias": "default",
        "collection": "teams",
        "indexes": [
            "name",
            "slug",
        ]
    }
