from datetime import datetime
import mongoengine

class Comment(mongoengine.Document):
    account = mongoengine.ReferenceField("User", required=True)
    subject = mongoengine.GenericReferenceField(required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.now)
    text = mongoengine.StringField(required=True)

    meta = {
        "alias": "default",
        "collection": "comments",
        "indexes": [
            "subject",
            "account",
            "rating",
        ]
    }

    def dict(self):
        return {
            "created": int(datetime.timestamp(self.created)),
            "updated": int(datetime.timestamp(self.updated)),
            "account": self.account.dict(),
            "text": self.text
        }
