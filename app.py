# from flask_socketio import SocketIO
# from core.interfaces import socket
from core.interfaces import rest
from flask_restful import Api
from flask_cors import CORS
from flask import Flask
import mongoengine
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
# sio = SocketIO(app, cors_allowed_origins='*')
api = Api(app)
CORS(app)

# socket.init(sio)
rest.init(api)

@app.route('/')
def root():
	return open('frontend/index.html').read()

if __name__ == '__main__':
	app.run(debug=config.debug, host=config.host, port=config.port)
	settings = dict(username=config.db['username'],
					password=config.db['password'],
					port=config.db['port'])

	mongoengine.register_connection(alias='default',
									name=config.db['name'],
									**settings)
