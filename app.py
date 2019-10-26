from flask import Flask
# from flask_socketio import SocketIO
from flask_restful import Api
from flask_cors import CORS
import core.db as dbmongo
# from core import socket
from core import rest
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
	return open('index.html').read()

if __name__ == '__main__':
	dbmongo.global_init()
	app.run(debug=config.debug, host=config.host, port=config.port)
