from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask_cors import CORS
from hikka import routes
from flask import Flask
import mongoengine
import config

# from hikka.modules import upload

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret
app.config["JSON_SORT_KEYS"] = False
CORS(app)

limiter = Limiter(
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

routes.init(app, limiter)
