from datetime import datetime
import mongoengine
import config

class File(mongoengine.Document):
    uploaded = mongoengine.BooleanField(required=True, default=False)
    account = mongoengine.ReferenceField("User", required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
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

    def link(self):
        """Return CDN link"""
        return config.cdn + self.path

    def path(self):
        """Return Spaces path"""
        name = config.spaces["name"]
        return f"/{name}/{self.path}"
