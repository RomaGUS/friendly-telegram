import mongoengine

class Vote(mongoengine.Document):
    anime = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "votes",
        "indexes": [
            "scope",
            "name",
        ]
    }

    def dict(self):
        return {
            "scope": self.scope,
            "name": self.name
        }
