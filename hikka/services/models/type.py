import mongoengine

class ReleaseType(mongoengine.Document):
    description = mongoengine.StringField(default=None)
    name = mongoengine.StringField(required=True)
    slug = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "types",
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
