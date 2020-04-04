import mongoengine

class Descriptor(mongoengine.Document):
    description = mongoengine.StringField(default=None)
    category = mongoengine.IntField(required=True)
    name = mongoengine.StringField(required=True)
    slug = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "descriptors",
        "indexes": [
            "category",
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
