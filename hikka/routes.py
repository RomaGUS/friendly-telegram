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

def init(api, app):
    # Auth routes
    api.add_resource(auth.Join, "/auth/join")
    api.add_resource(auth.Login, "/auth/login")
    api.add_resource(auth.Activate, "/auth/activate")
    api.add_resource(auth.RequestReset, "/auth/reset/request")
    api.add_resource(auth.PasswordReset, "/auth/reset")

    # Account routes
    api.add_resource(account.PasswordChange, "/account/password")
    api.add_resource(account.AccountTeams, "/account/teams")

    # Team routes
    api.add_resource(teams.NewTeam, "/teams/new")
    api.add_resource(teams.EditTeam, "/teams/edit")
    api.add_resource(teams.GetTeam, "/teams/get/<string:slug>")
    api.add_resource(teams.AddMember, "/teams/member/add")
    api.add_resource(teams.RemoveMember, "/teams/member/remove")
    api.add_resource(teams.TeamUpload, "/teams/upload")
    api.add_resource(teams.ListTeams, "/teams/list")

    # Descriptor routes
    api.add_resource(descriptors.NewDescriptor, "/descriptors/new")
    api.add_resource(descriptors.UpdateDescriptor, "/descriptors/update")

    # Anime routes
    api.add_resource(anime.NewAnime, "/anime/new")
    api.add_resource(anime.EditAnime, "/anime/edit")
    api.add_resource(anime.GetAnime, "/anime/get/<string:slug>")
    api.add_resource(anime.AnimeUpload, "/anime/upload")
    api.add_resource(anime.Selected, "/anime/selected")
    api.add_resource(anime.Search, "/anime/list")

    # Episode routes
    api.add_resource(episodes.AddEpisode, "/episodes/add")
    api.add_resource(episodes.UpdateEpisode, "/episodes/update")
    api.add_resource(episodes.DeleteEpisode, "/episodes/delete")

    # System routes
    api.add_resource(system.ManagePermissions, "/system/permissions/manage")
    api.add_resource(system.UserPermissions, "/system/permissions/user")
    api.add_resource(system.StaticData, "/system/static")

    # Comment routes
    api.add_resource(comments.NewComment, "/comments/new")
    api.add_resource(comments.UpdateComment, "/comments/update")
    api.add_resource(comments.ListComments, "/comments/list")

    # Voting routes
    api.add_resource(statuses.Update, "/status")
    api.add_resource(statuses.Check, "/status/check")

    @app.route("/")
    def root():
        return flask.render_template("docs.html")

    @app.errorhandler(400)
    def error400(error):
        return errors.abort("general", "bad-request", 400)

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
