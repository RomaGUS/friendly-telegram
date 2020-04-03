import mongoengine

choices = ("franchise")

class Descriptor(mongoengine.Document):
    category = mongoengine.StringField(required=True, choices=choices)
    description = mongoengine.StringField(default=None)
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
