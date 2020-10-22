from flask_limiter.util import get_remote_address
from flask import Flask, render_template
# from hikka.modules import comments
from hikka.modules import account
from hikka.modules import errors
from hikka.modules import auth
from flask_cors import CORS
import flask_limiter
import mongoengine
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret
app.config["JSON_SORT_KEYS"] = False
CORS(app)

limiter = flask_limiter.Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=config.limits
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

# App blueprints
app.register_blueprint(account.blueprint, url_prefix="/account")
app.register_blueprint(auth.blueprint, url_prefix="/auth")
app.register_blueprint(errors.blueprint)

@app.route("/")
def docs():
    return render_template("docs.html")
