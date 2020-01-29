from hikka.services.models.type import ReleaseType
from hikka.services.models.comment import Comment
from hikka.services.models.genre import Genre
from hikka.services.models.team import Team
from datetime import datetime
import mongoengine

class Release(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    slug = mongoengine.StringField(required=True)
    rtype = mongoengine.ReferenceField(ReleaseType, required=True)
    hidden = mongoengine.BooleanField(required=True, default=False)
    description = mongoengine.StringField(required=True, default=None)
    genres = mongoengine.ListField(mongoengine.ReferenceField(Genre))
    teams = mongoengine.ListField(mongoengine.ReferenceField(Team))
    created = mongoengine.DateTimeField(default=datetime.now)
    comments = mongoengine.EmbeddedDocumentListField(Comment)
    views = mongoengine.IntField(default=0)

    meta = {
        "alias": "default",
        "collection": "releases",
        "indexes": [
            "name",
            "slug",
            "genres",
        ]
    }
