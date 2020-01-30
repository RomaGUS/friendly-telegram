from hikka.services.models.type import ReleaseType
from hikka.services.models.genre import Genre
from hikka.services.models.team import Team
from hikka.services.models.user import User
from datetime import datetime
import mongoengine

class Comment(mongoengine.EmbeddedDocument):
    text = mongoengine.StringField(required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
    hidden = mongoengine.BooleanField(required=True, default=False)
    account = mongoengine.ReferenceField(User)

class Title(mongoengine.EmbeddedDocument):
    ua = mongoengine.StringField(required=True)
    jp = mongoengine.StringField(default=None)

    def dict(self):
        return {
            "ua": self.ua,
            "jp": self.jp
        }

class Release(mongoengine.Document):
    title = mongoengine.EmbeddedDocumentField(Title, required=True)
    rtype = mongoengine.ReferenceField(ReleaseType, required=True)
    hidden = mongoengine.BooleanField(required=True, default=False)
    description = mongoengine.StringField(required=True, default=None)
    genres = mongoengine.ListField(mongoengine.ReferenceField(Genre))
    teams = mongoengine.ListField(mongoengine.ReferenceField(Team))
    created = mongoengine.DateTimeField(default=datetime.now)
    comments = mongoengine.EmbeddedDocumentListField(Comment)
    slug = mongoengine.StringField(required=True)
    views = mongoengine.IntField(default=0)

    meta = {
        "alias": "default",
        "collection": "releases",
        "indexes": [
            "slug",
            "genres",
            "title.jp",
            "title.ua",
        ]
    }
