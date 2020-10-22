from flask_limiter.util import get_remote_address
from flask import Flask, render_template
# from hikka.modules import descriptors
# from hikka.modules import comments
# from hikka.modules import statuses
# from hikka.modules import episodes
# from hikka.modules import account
# from hikka.modules import errors
# from hikka.modules import upload
# from hikka.modules import system
# from hikka.modules import anime
# from hikka.modules import teams
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
app.register_blueprint(auth.blueprint, url_prefix="/auth")
# app.register_blueprint(descriptors.blueprint)
# app.register_blueprint(comments.blueprint)
# app.register_blueprint(episodes.blueprint)
# app.register_blueprint(statuses.blueprint)
# app.register_blueprint(account.blueprint)
# app.register_blueprint(errors.blueprint)
# app.register_blueprint(system.blueprint)
# app.register_blueprint(upload.blueprint)
# app.register_blueprint(teams.blueprint)
# app.register_blueprint(anime.blueprint)

# Limiter exemptions
# limiter.exempt(upload.blueprint)

@app.route("/")
def docs():
    return render_template("docs.html")
