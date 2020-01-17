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

@app.route("/")
def home():
    return render_template("home.html", title="Home page")

@app.route("/about")
def about():
    return render_template("about.html")
