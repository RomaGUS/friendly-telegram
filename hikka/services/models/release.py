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

class Episode(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(required=True, default=None)
    position = mongoengine.IntField(required=True)
    video = mongoengine.ReferenceField("File")

class Release(mongoengine.Document):
    title = mongoengine.EmbeddedDocumentField(Title, required=True)
    hidden = mongoengine.BooleanField(required=True, default=False)
    category = mongoengine.ReferenceField("Category", required=True)
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

    episodes = mongoengine.SortedListField(
        mongoengine.EmbeddedDocumentField(Episode),
        ordering="position"
    )

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

    def dict(self):
        data = {
            "description": self.description,
            "title": self.title.dict(),
            "category": self.category.dict(),
            "state": self.state.dict(),
            "slug": self.slug,
            "poster": None,
            "subtitles": [],
            "voiceover": [],
            "genres": [],
            "teams": []
        }

        for account in self.subtitles:
            data["subtitles"].append(account.dict())

        for account in self.voiceover:
            data["voiceover"].append(account.dict())

        for genre in self.genres:
            data["genres"].append(genre.dict())

        for team in self.teams:
            data["teams"].append(team.dict())

        if self.poster is not None:
            if self.poster.uploaded is True:
                data["poster"] = self.poster.link()

        return data
