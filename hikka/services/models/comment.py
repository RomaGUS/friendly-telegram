from hikka.services.models.user import User
from datetime import datetime
import mongoengine

class Balance(mongoengine.EmbeddedDocument):
    text = mongoengine.StringField(required=True)
    created = mongoengine.DateTimeField(default=datetime.now)
    hidden = mongoengine.BooleanField(required=True, default=False)
    account = mongoengine.ReferenceField(User)
