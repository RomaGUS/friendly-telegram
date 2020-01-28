from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret
api = Api(app)
CORS(app)

from hikka.modules import auth
from hikka.modules import files
from hikka.modules import teams
from hikka.modules import genres

@app.route("/")
def root():
    return render_template("index.html")
