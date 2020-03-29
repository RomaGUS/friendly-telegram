from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask_cors import CORS
from hikka import errors
from flask import Flask
import flask_restful
import mongoengine
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret
api = errors.Api(app)
CORS(app)

flask_restful.abort = errors.reqparse_abort
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

from hikka import routes
routes.init(api, app)
