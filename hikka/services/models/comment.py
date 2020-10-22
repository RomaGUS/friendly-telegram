from datetime import datetime
import mongoengine

class Comment(mongoengine.Document):
    account = mongoengine.ReferenceField("User", required=True)
    subject = mongoengine.GenericReferenceField(required=True)
    created = mongoengine.DateTimeField(default=datetime.utcnow)
    updated = mongoengine.DateTimeField(default=datetime.utcnow)
    text = mongoengine.StringField(required=True)
    counter = mongoengine.SequenceField()

    meta = {
        "alias": "default",
        "collection": "comments",
        "indexes": [
            "subject",
            "account",
        ],
        "ordering": ["-counter"]
    }

    def dict(self):
        return {
            "created": int(datetime.timestamp(self.created)),
            "updated": int(datetime.timestamp(self.updated)),
            "account": self.account.dict(),
            "counter": self.counter,
            "text": self.text
        }
