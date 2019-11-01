import mongoengine
from datetime import datetime

class Video(mongoengine.Document):
	created = mongoengine.DateTimeField(default=datetime.now)
	uploaded = mongoengine.BooleanField(required=True, default=False)
	name = mongoengine.StringField(required=True)

	meta = {
		'alias': 'default',
		'collection': 'videos',
		'indexes': [
			'created',
		],
		'ordering': ['-created']
	}
