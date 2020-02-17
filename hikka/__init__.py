from flask_limiter.util import get_remote_address
from flask import Flask, render_template
from flask_limiter import Limiter
from flask_cors import CORS
from hikka import errors
import flask_restful
import mongoengine
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret
api = errors.Api(app)
CORS(app)

flask_restful.abort = errors.reqparse_abort
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["6/second"]
)

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

@app.errorhandler(405)
def error405(error):
    return errors.abort("general", "method-not-allowed", 405)

@app.errorhandler(429)
def error429(error):
    return errors.abort("general", "too-many-requests", 429)
