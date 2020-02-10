from datetime import datetime
import mongoengine

class Comment(mongoengine.EmbeddedDocument):
    text = mongoengine.StringField(required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
    hidden = mongoengine.BooleanField(required=True, default=False)
    account = mongoengine.ReferenceField("User")

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
    hidden = mongoengine.BooleanField(required=True, default=False)
    rtype = mongoengine.ReferenceField("ReleaseType", required=True)
    description = mongoengine.StringField(required=True, default=None)
    subtitles = mongoengine.ListField(mongoengine.ReferenceField("User"))
    voiceover = mongoengine.ListField(mongoengine.ReferenceField("User"))
    genres = mongoengine.ListField(mongoengine.ReferenceField("Genre"))
    teams = mongoengine.ListField(mongoengine.ReferenceField("Team"))
    state = mongoengine.ReferenceField("State", required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
    comments = mongoengine.EmbeddedDocumentListField(Comment)
    slug = mongoengine.StringField(required=True)
    poster = mongoengine.ReferenceField("File")
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
