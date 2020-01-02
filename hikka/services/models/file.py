import mongoengine
from datetime import datetime

class File(mongoengine.Document):
	created = mongoengine.DateTimeField(default=datetime.now)
	uploaded = mongoengine.BooleanField(required=True, default=False)
	name = mongoengine.StringField()
	path = mongoengine.StringField()
	mime = mongoengine.StringField()
	tmp = mongoengine.StringField()

	meta = {
		'alias': 'default',
		'collection': 'files',
		'indexes': [
			'created',
		],
		'ordering': ['-created']
	}
