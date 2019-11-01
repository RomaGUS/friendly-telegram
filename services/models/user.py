import mongoengine
from datetime import datetime
from services.models.permission import Permission

class User(mongoengine.Document):
	permissions = mongoengine.ListField(mongoengine.ReferenceField(Permission))
	created = mongoengine.DateTimeField(default=datetime.now)
	login = mongoengine.DateTimeField(default=datetime.now)
	username = mongoengine.StringField(required=True)
	password = mongoengine.StringField(required=True, max_length=64)
	email = mongoengine.StringField(required=True)

	meta = {
		'alias': 'default',
		'collection': 'users',
		'indexes': [
			'created',
			'username',
			'email',
			'login',
		],
		'ordering': ['-created']
	}
