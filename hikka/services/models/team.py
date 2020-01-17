from hikka.services.models.user import User
import mongoengine

class Team(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    slug = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    members = mongoengine.ListField(mongoengine.ReferenceField(User))
    hidden = mongoengine.BooleanField(required=True, default=False)
    # ToDo: cover image with files

    meta = {
        "alias": "default",
        "collection": "teams",
        "indexes": [
            "name",
            "slug",
        ]
    }
