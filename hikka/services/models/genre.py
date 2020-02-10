import mongoengine

class Genre(mongoengine.Document):
    description = mongoengine.StringField(default=None)
    name = mongoengine.StringField(required=True)
    slug = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "genres",
        "indexes": [
            "name",
            "slug",
        ]
    }

    def dict(self):
        return {
            "description": self.description,
            "name": self.name,
            "slug": self.slug
        }
