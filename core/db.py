import mongoengine
import config

def global_init():
	settings = dict(username=config.db['username'],
					password=config.db['password'],
					port=config.db['port'])

	mongoengine.register_connection(alias='default',
									name=config.db['name'],
									**settings)
