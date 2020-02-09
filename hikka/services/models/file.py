from hikka.services.models.user import User
from datetime import datetime
import mongoengine
import config

class File(mongoengine.Document):
    uploaded = mongoengine.BooleanField(required=True, default=False)
    created = mongoengine.DateTimeField(default=datetime.now)
    account = mongoengine.ReferenceField(User, required=True)
    path = mongoengine.StringField()
    name = mongoengine.StringField()

    meta = {
        "alias": "default",
        "collection": "files",
        "indexes": [
            "created",
        ],
        "ordering": ["-created"]
    }

    def link(self):
        return config.cdn + self.path
