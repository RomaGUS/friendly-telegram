from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
api = Api(app)
CORS(app)

from hikka.interfaces import rest

@app.route('/')
def root():
	return render_template('index.html')
