from datetime import datetime
from hikka import static
import mongoengine

class External(mongoengine.EmbeddedDocument):
    myanimelist = mongoengine.IntField(default=None)
    toloka = mongoengine.IntField(default=None)

    def dict(self):
        data = {
            "myanimelist": None,
            "toloka": None
        }

        if self.myanimelist:
            data["myanimelist"] = f"https://myanimelist.net/anime/{self.myanimelist}"

        if self.toloka:
            data["toloka"] = f"https://toloka.to/t{self.toloka}"

        return data

class Episode(mongoengine.EmbeddedDocument):
    description = mongoengine.StringField(default=None)
    position = mongoengine.IntField(required=True)
    name = mongoengine.StringField(default=None)
    video = mongoengine.ReferenceField("File")

    def dict(self):
        return {
            "description": self.description,
            "video": self.video.link(),
            "position": self.position,
            "name": self.name
        }

class Title(mongoengine.EmbeddedDocument):
    ua = mongoengine.StringField(required=True)
    jp = mongoengine.StringField(default=None)

    def dict(self):
        return {
            "ua": self.ua,
            "jp": self.jp
        }

class Anime(mongoengine.Document):
    title = mongoengine.EmbeddedDocumentField(Title, required=True)
    hidden = mongoengine.BooleanField(required=True, default=False)
    selected = mongoengine.BooleanField(required=True, default=False)
    description = mongoengine.StringField(required=True, default=None)
    subtitles = mongoengine.ListField(mongoengine.ReferenceField("User"))
    voiceover = mongoengine.ListField(mongoengine.ReferenceField("User"))
    teams = mongoengine.ListField(mongoengine.ReferenceField("Team"))
    created = mongoengine.DateTimeField(default=datetime.now)
    slug = mongoengine.StringField(required=True)
    poster = mongoengine.ReferenceField("File")
    banner = mongoengine.ReferenceField("File")
    views = mongoengine.IntField(default=0)

    season = mongoengine.IntField(default=None, min_value=1, max_value=4)
    year = mongoengine.IntField(default=datetime.now().year)
    total = mongoengine.IntField(default=None)

    franchises = mongoengine.ListField(mongoengine.ReferenceField("Descriptor", reverse_delete_rule=4))
    genres = mongoengine.ListField(mongoengine.IntField(required=True))
    category = mongoengine.IntField(required=True)
    state = mongoengine.IntField(required=True)

    aliases = mongoengine.ListField(mongoengine.StringField())
    external = mongoengine.EmbeddedDocumentField(External)
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

    def missing(self):
        missing = False

        if self.external is None:
            self.external = External()
            missing = True

        if missing:
            self.save()

    def dict(self, episodes=False):
        self.missing()

        category = static.dict(static.categories, self.category)
        state = static.dict(static.states, self.state)

        data = {
            "description": self.description,
            "title": self.title.dict(),
            "external": self.external.dict(),
            "rating": float(self.rating),
            "aliases": self.aliases,
            "season": self.season,
            "slug": self.slug,
            "year": self.year,
            "poster": None,
            "banner": None,
            "franchises": [],
            "subtitles": [],
            "voiceover": [],
            "genres": [],
            "teams": [],
            "episodes": {
                "released": len(self.episodes),
                "total": self.total
            },
            "category": category,
            "state": state
        }

        for account in self.subtitles:
            data["subtitles"].append(account.dict())

        for account in self.voiceover:
            data["voiceover"].append(account.dict())

        for franchise in self.franchises:
            data["franchises"].append(franchise.dict())

        for team in self.teams:
            data["teams"].append(team.dict())

        for genre in self.genres:
            item = static.dict(static.genres, genre)
            data["genres"].append(item)

        if self.poster:
            if self.poster.uploaded is True:
                data["poster"] = self.poster.link()

        if self.banner:
            if self.poster.uploaded is True:
                data["banner"] = self.banner.link()

        if episodes:
            data["episodes"]["list"] = []

            for episode in self.episodes:
                data["episodes"]["list"].append(episode.dict())

        return data
