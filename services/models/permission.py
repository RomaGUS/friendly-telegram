import mongoengine

class UserPermission(mongoengine.Document):
	scope = mongoengine.StringField(required=True)
	name = mongoengine.StringField(required=True)

	meta = {
		'alias': 'default',
		'collection': 'rights',
		'indexes': [
			'scope',
			'name',
		]
	}
