from hikka.services.permissions import PermissionService
from hikka.services.categories import CategoryService
from hikka.services.releases import ReleaseService
from werkzeug.datastructures import FileStorage
from hikka.services.genres import GenreService
from hikka.services.states import StateService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from hikka.decorators import auth_required
from hikka.upload import UploadHelper
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import Response
from flask import request

class NewRelease(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("subtitles", type=list, default=[], location="json")
        parser.add_argument("voiceover", type=list, default=[], location="json")
        parser.add_argument("genres", type=list, default=[], location="json")
        parser.add_argument("poster", type=FileStorage, location="files")
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("category", type=str, required=True)
        parser.add_argument("title", type=dict, required=True)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("team", type=str, required=True)
        parser.add_argument("state", type=str, default=None)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        title_parser = reqparse.RequestParser()
        title_parser.add_argument("jp", type=str, default=None, location=("title",))
        title_parser.add_argument("ua", type=str, location=("title",))
        title_args = title_parser.parse_args(req=args)

        team = TeamService.get_by_slug(args["team"])
        if team is None:
            return abort("team", "not-found")

        if not PermissionService.check(request.account, f"team-{team.slug}", "admin"):
            return abort("account", "permission")

        release = ReleaseService.get_by_slug(args["slug"])
        if release is not None:
            return abort("release", "slug-exists")

        category = CategoryService.get_by_slug(args["category"])
        if category is None:
            return abort("category", "not-found")

        state = StateService.get_by_slug(args["state"])
        if state is None:
            return abort("state", "not-found")

        if args["description"] is None:
            return abort("general", "missing-field")

        poster = None
        if args["poster"] is not None:
            helper = UploadHelper(request.account, args["poster"], "poster")
            data = helper.upload_image()

            if type(data) is Response:
                return data

            poster = data

        genres = []
        for slug in args["genres"]:
            genre = GenreService.get_by_slug(slug)
            if genre is not None:
                genres.append(genre)

            else:
                return abort("genre", "not-found")

        subtitles = []
        for username in args["subtitles"]:
            subtitles_account = UserService.get_by_username(username)
            if subtitles_account is not None:
                subtitles.append(subtitles_account)

            else:
                return abort("account", "not-found")

        voiceover = []
        for username in args["voiceover"]:
            voiceover_account = UserService.get_by_username(username)
            if voiceover_account is not None:
                voiceover.append(voiceover_account)

            else:
                return abort("account", "not-found")

        title = ReleaseService.get_title(title_args["ua"], title_args["jp"])
        release = ReleaseService.create(
            title,
            args["slug"],
            args["description"],
            category,
            state,
            genres,
            [team],
            subtitles,
            voiceover
        )

        if poster is not None:
            ReleaseService.update_poster(release, poster)

        result["data"] = release.dict()
        return result

class GetRelease(Resource):
    def get(self, slug):
        release = ReleaseService.get_by_slug(slug)
        if release is None:
            return abort("release", "not-found")

        return release.dict(True)

class ReleasesList(Resource):
    def get(self):
        result = {"error": None, "data": []}

        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int, default=0)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        releases = ReleaseService.list(args["page"])

        for release in releases:
            result["data"].append(release.dict())

        return result
