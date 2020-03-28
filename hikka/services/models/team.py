import mongoengine

class Team(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    slug = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    members = mongoengine.ListField(mongoengine.ReferenceField("User"))
    hidden = mongoengine.BooleanField(required=True, default=False)
    avatar = mongoengine.ReferenceField("File")

    meta = {
        "alias": "default",
        "collection": "teams",
        "indexes": [
            "name",
            "slug",
        ]
    }

    def dict(self, members=False):
        avatar = self.avatar.link() if self.avatar else None
        data = {
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "avatar": avatar
        }

        if members:
            data["members"] = []
            for member in self.members:
                data["members"].append(member.dict())

        return data
