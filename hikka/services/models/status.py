from datetime import datetime
from hikka import static
import mongoengine

class Status(mongoengine.Document):
    account = mongoengine.ReferenceField("User", required=True)
    subject = mongoengine.GenericReferenceField(required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
    rating = mongoengine.IntField(min_value=1, max_value=10)
    content = mongoengine.IntField(required=True)
    position = mongoengine.IntField(default=None)
    status = mongoengine.IntField(default=None)
    times = mongoengine.IntField(default=0)

    meta = {
        "alias": "default",
        "collection": "statuses",
        "indexes": [
            "subject",
            "account",
            "rating",
            "status",
        ],
        "ordering": ["-created"]
    }

    def dict(self):
        content = static.slug("content", self.content)
        return {
            "content": content["slug"],
            "created": int(datetime.timestamp(self.created)),
            "position": self.position,
            "rating": self.rating,
            "times": self.times
        }
