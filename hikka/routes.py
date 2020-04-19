from hikka.modules import descriptors
from hikka.modules import comments
from hikka.modules import statuses
from hikka.modules import episodes
from hikka.modules import account
from hikka.modules import upload
from hikka.modules import system
from hikka.modules import anime
from hikka.modules import teams
from hikka.modules import auth
from hikka import errors
import flask

def add_resource(app, view, endpoint):
    app.add_url_rule(endpoint, view_func=view.as_view(endpoint))

def init(app, limiter):
    # App blueprints
    app.register_blueprint(descriptors.blueprint)
    app.register_blueprint(comments.blueprint)
    app.register_blueprint(episodes.blueprint)
    app.register_blueprint(statuses.blueprint)
    app.register_blueprint(account.blueprint)
    app.register_blueprint(system.blueprint)
    app.register_blueprint(upload.blueprint)
    app.register_blueprint(teams.blueprint)
    app.register_blueprint(anime.blueprint)
    app.register_blueprint(auth.blueprint)

    # Limiter exemptions
    limiter.exempt(upload.blueprint)

    # Misc routes
    @app.route("/")
    def docs():
        return flask.render_template("docs.html")

    @app.errorhandler(400)
    def error400(error):
        return errors.abort("general", "bad-request", 400)

    @app.errorhandler(422)
    def error422(error):
        return errors.abort("general", "missing-field", 422)

    @app.errorhandler(404)
    def error404(error):
        return errors.abort("general", "not-found", 404)

    @app.errorhandler(405)
    def error405(error):
        return errors.abort("general", "method-not-allowed", 405)

    @app.errorhandler(429)
    def error429(error):
        return errors.abort("general", "too-many-requests", 429)

    @app.errorhandler(500)
    def error500(error):
        return errors.abort("general", "something-bad", 500)
