import mongoengine
from datetime import datetime

class User(mongoengine.Document):
	created = mongoengine.DateTimeField(default=datetime.now)
	username = mongoengine.StringField(required=True)
	password = mongoengine.StringField(required=True, max_length=64)
	email = mongoengine.StringField(required=True)
	banned = mongoengine.BooleanField(required=True, default=False)
	activated = mongoengine.BooleanField(required=True, default=True)
	admin = mongoengine.BooleanField(required=True, default=False)
	role = mongoengine.StringField(required=True, default='user')
	login = mongoengine.DateTimeField(default=datetime.now)

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
