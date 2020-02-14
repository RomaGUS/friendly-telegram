from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
import mongoengine
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret
api = Api(app)
CORS(app)

db_settings = dict(
    username=config.db["username"],
    password=config.db["password"],
    port=config.db["port"]
)

mongoengine.register_connection(
    alias="default",
    name=config.db["name"],
    **db_settings
)

from hikka import routes

@app.route("/")
def root():
    return render_template("index.html")
