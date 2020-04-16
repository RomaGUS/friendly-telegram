from hikka.modules import descriptors
from hikka.modules import comments
from hikka.modules import statuses
from hikka.modules import episodes
from hikka.modules import account
from hikka.modules import system
from hikka.modules import anime
from hikka.modules import teams
from hikka.modules import auth
from hikka import errors
import flask

def add_resource(app, view, endpoint):
    app.add_url_rule(endpoint, view_func=view.as_view(endpoint))

def init(app):
    # Auth routes
    add_resource(app, auth.Join, "/auth/join")
    add_resource(app, auth.Login, "/auth/login")
    add_resource(app, auth.Activate, "/auth/activate")
    add_resource(app, auth.RequestReset, "/auth/reset/request")
    add_resource(app, auth.PasswordReset, "/auth/reset")

    # Account routes
    add_resource(app, account.PasswordChange, "/account/password")
    add_resource(app, account.AccountTeams, "/account/teams")

    # Team routes
    add_resource(app, teams.NewTeam, "/teams/new")
    add_resource(app, teams.EditTeam, "/teams/edit")
    add_resource(app, teams.GetTeam, "/teams/get/<string:slug>")
    add_resource(app, teams.AddMember, "/teams/member/add")
    add_resource(app, teams.RemoveMember, "/teams/member/remove")
    add_resource(app, teams.TeamUpload, "/teams/upload")
    add_resource(app, teams.ListTeams, "/teams/list")

    # Descriptor routes
    add_resource(app, descriptors.NewDescriptor, "/descriptors/new")
    add_resource(app, descriptors.UpdateDescriptor, "/descriptors/update")

    # Anime routes
    add_resource(app, anime.NewAnime, "/anime/new")
    add_resource(app, anime.EditAnime, "/anime/edit")
    add_resource(app, anime.GetAnime, "/anime/get/<string:slug>")
    add_resource(app, anime.AnimeUpload, "/anime/upload")
    add_resource(app, anime.Selected, "/anime/selected")
    add_resource(app, anime.Search, "/anime/list")

    # Episode routes
    add_resource(app, episodes.AddEpisode, "/episodes/add")
    add_resource(app, episodes.UpdateEpisode, "/episodes/update")
    add_resource(app, episodes.DeleteEpisode, "/episodes/delete")
    add_resource(app, episodes.EpisodeUpload, "/episodes/upload")

    # System routes
    add_resource(app, system.ManagePermissions, "/system/permissions/manage")
    add_resource(app, system.UserPermissions, "/system/permissions/user")
    add_resource(app, system.StaticData, "/system/static")

    # Comment routes
    add_resource(app, comments.NewComment, "/comments/new")
    add_resource(app, comments.UpdateComment, "/comments/update")
    add_resource(app, comments.ListComments, "/comments/list")

    # Voting routes
    add_resource(app, statuses.Update, "/status")
    add_resource(app, statuses.Check, "/status/check")

    @app.route("/")
    def root():
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
