from datetime import datetime
import mongoengine

# class Comment(mongoengine.EmbeddedDocument):
#     text = mongoengine.StringField(required=True)
#     created = mongoengine.DateTimeField(default=datetime.now)
#     hidden = mongoengine.BooleanField(required=True, default=False)
#     account = mongoengine.ReferenceField("User")

class Title(mongoengine.EmbeddedDocument):
    ua = mongoengine.StringField(required=True)
    jp = mongoengine.StringField(default=None)

    def dict(self):
        return {
            "ua": self.ua,
            "jp": self.jp
        }

class Episode(mongoengine.EmbeddedDocument):
    position = mongoengine.IntField(required=True)
    name = mongoengine.StringField(default=None)
    video = mongoengine.ReferenceField("File")

    def dict(self):
        return {
            "video": self.video.link(),
            "position": self.position,
            "name": self.name
        }

class Anime(mongoengine.Document):
    title = mongoengine.EmbeddedDocumentField(Title, required=True)
    hidden = mongoengine.BooleanField(required=True, default=False)
    description = mongoengine.StringField(required=True, default=None)
    subtitles = mongoengine.ListField(mongoengine.ReferenceField("User"))
    voiceover = mongoengine.ListField(mongoengine.ReferenceField("User"))
    teams = mongoengine.ListField(mongoengine.ReferenceField("Team"))
    created = mongoengine.DateTimeField(default=datetime.now)
    slug = mongoengine.StringField(required=True)
    poster = mongoengine.ReferenceField("File")
    views = mongoengine.IntField(default=0)

    genres = mongoengine.ListField(mongoengine.ReferenceField("Descriptor", reverse_delete_rule=4))
    franchises = mongoengine.ListField(mongoengine.ReferenceField("Descriptor", reverse_delete_rule=4))
    category = mongoengine.ReferenceField("Descriptor", reverse_delete_rule=4, required=True)
    state = mongoengine.ReferenceField("Descriptor", reverse_delete_rule=4, required=True)

    aliases = mongoengine.ListField(mongoengine.StringField())
    rating = mongoengine.DecimalField(default=0)
    search = mongoengine.StringField()

    episodes = mongoengine.SortedListField(
        mongoengine.EmbeddedDocumentField(Episode),
        ordering="position"
    )

    meta = {
        "alias": "default",
        "collection": "anime",
        "indexes": [
            "slug",
            "genres",
            "category",
            "state",
            "title.jp",
            "title.ua",
            "search",
            "rating",
        ]
    }

    def dict(self, episodes=False):
        print()
        data = {
            "description": self.description,
            "title": self.title.dict(),
            "category": self.category.dict(),
            "rating": float(self.rating),
            "state": self.state.dict(),
            "slug": self.slug,
            "poster": None,
            "subtitles": [],
            "voiceover": [],
            "genres": [],
            "franchises": [],
            "teams": []
        }

        for account in self.subtitles:
            data["subtitles"].append(account.dict())

        for account in self.voiceover:
            data["voiceover"].append(account.dict())

        for genre in self.genres:
            data["genres"].append(genre.dict())

        for franchise in self.franchises:
            data["franchises"].append(franchise.dict())

        for team in self.teams:
            data["teams"].append(team.dict())

        if self.poster is not None:
            if self.poster.uploaded is True:
                data["poster"] = self.poster.link()

        if episodes:
            data["episodes"] = []

            for episode in self.episodes:
                data["episodes"].append(episode.dict())

        return data
