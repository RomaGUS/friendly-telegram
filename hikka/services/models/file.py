from datetime import datetime
import mongoengine
import config

class File(mongoengine.Document):
    uploaded = mongoengine.BooleanField(required=True, default=False)
    account = mongoengine.ReferenceField("User", required=True)
    created = mongoengine.DateTimeField(default=datetime.utcnow)
    path = mongoengine.StringField(default=None)
    name = mongoengine.StringField(default=None)

    meta = {
        "alias": "default",
        "collection": "files",
        "indexes": [
            "created",
        ],
        "ordering": ["-created"]
    }

    def is_link(self):
        return self.path[:4] == "http"

    def link(self):
        """Return CDN link"""
        if self.path is None:
            return None

        if self.is_link():
            return self.path

        return config.cdn + self.path

    def storage(self):
        """Return S3 path"""
        return config.storage["name"] + self.path
