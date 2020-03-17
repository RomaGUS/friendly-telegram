from datetime import datetime
import mongoengine

class Vote(mongoengine.Document):
    rating = mongoengine.IntField(min_value=1, max_value=10, required=True)
    account = mongoengine.ReferenceField("User", required=True)
    subject = mongoengine.GenericReferenceField(required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.now)

    meta = {
        "alias": "default",
        "collection": "votes",
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
            "subject": self.subject.dict(),
            "rating": self.rating
        }
