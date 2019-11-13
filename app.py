from hikka import app
import mongoengine
import config

if __name__ == '__main__':
	db_settings = dict(username=config.db['username'],
					password=config.db['password'],
					port=config.db['port'])

	mongoengine.register_connection(alias='default',
									name=config.db['name'],
									**db_settings)

	app.run(debug=config.debug, host=config.host, port=config.port)
