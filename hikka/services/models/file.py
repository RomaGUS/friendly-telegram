from datetime import datetime
import mongoengine
import config

class File(mongoengine.Document):
    uploaded = mongoengine.BooleanField(required=True, default=False)
    account = mongoengine.ReferenceField("User", required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
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
