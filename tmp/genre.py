import mongoengine

class Genre(mongoengine.Document):
	name = mongoengine.StringField(required=True)
	description = mongoengine.StringField(required=True)
	slug = mongoengine.StringField(required=True)

	meta = {
		'alias': 'default',
		'collection': 'genres',
		'indexes': [
			'name',
			'slug',
		]
	}
