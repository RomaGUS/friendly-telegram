from datetime import datetime
import mongoengine

class User(mongoengine.Document):
    permissions = mongoengine.ListField(mongoengine.ReferenceField("Permission"))
    password = mongoengine.StringField(required=True, max_length=64)
    created = mongoengine.DateTimeField(default=datetime.utcnow)
    reset = mongoengine.DateTimeField(default=datetime.utcnow)
    login = mongoengine.DateTimeField(default=datetime.utcnow)
    username = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    avatar = mongoengine.ReferenceField("File")

    meta = {
        "alias": "default",
        "collection": "users",
        "indexes": [
            "created",
            "username",
            "email",
            "login",
        ],
        "ordering": ["-created"]
    }

    def list_permissions(self):
        result = []
        for permission in self.permissions:
            result.append(permission.dict())

        return result

    def dict(self):
        avatar = self.avatar.link() if self.avatar else None
        return {
            "login": int(datetime.timestamp(self.login)),
            "username": self.username,
            "avatar": avatar
        }
