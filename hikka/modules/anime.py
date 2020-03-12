from hikka.services.permissions import PermissionService
from hikka.services.descriptors import DescriptorService
from werkzeug.datastructures import FileStorage
from hikka.services.anime import AnimeService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from hikka.tools.upload import UploadHelper
from hikka.decorators import auth_required
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import Response
from flask import request
from hikka import utils

class NewAnime(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("subtitles", type=list, default=[], location="json")
        parser.add_argument("voiceover", type=list, default=[], location="json")
        parser.add_argument("aliases", type=list, default=[], location="json")
        parser.add_argument("genres", type=list, default=[], location="json")
        parser.add_argument("poster", type=FileStorage, location="files")
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("category", type=str, required=True)
        parser.add_argument("title", type=dict, required=True)
        parser.add_argument("team", type=str, required=True)
        parser.add_argument("state", type=str, default=None)
        args = parser.parse_args()

        title_parser = reqparse.RequestParser()
        title_parser.add_argument("jp", type=str, default=None, location=("title",))
        title_parser.add_argument("ua", type=str, location=("title",))
        title_args = title_parser.parse_args(req=args)

        for alias in args["aliases"]:
            if type(alias) is not str:
                return abort("general", "alias-invalid-type")

        team = TeamService.get_by_slug(args["team"])
        if team is None:
            return abort("team", "not-found")

        if request.account not in team.members:
            return abort("account", "not-team-member")

        if not PermissionService.check(request.account, "global", "publishing"):
            return abort("account", "permission")

        category = DescriptorService.get_by_slug("category", args["category"])
        if category is None:
            return abort("category", "not-found")

        state = DescriptorService.get_by_slug("state", args["state"])
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
            genre = DescriptorService.get_by_slug("genre", slug)
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

        title = AnimeService.get_title(title_args["ua"], title_args["jp"])
        search = utils.create_search(title_args["ua"], title_args["jp"], args["aliases"])
        slug = utils.create_slug(title_args["ua"])

        anime = AnimeService.create(
            title,
            slug,
            args["description"],
            search,
            category,
            state,
            genres,
            [team],
            subtitles,
            voiceover,
            args["aliases"]
        )

        if poster is not None:
            AnimeService.update_poster(anime, poster)

        result["data"] = anime.dict()
        return result

class GetAnime(Resource):
    def get(self, slug):
        anime = AnimeService.get_by_slug(slug)
        if anime is None:
            return abort("anime", "not-found")

        return anime.dict(True)

class AnimesList(Resource):
    def get(self):
        result = {"error": None, "data": []}

        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int, default=0)
        args = parser.parse_args()

        anime = AnimeService.list(args["page"])
        for anime in anime:
            result["data"].append(anime.dict())

        return result

class Search(Resource):
    def post(self):
        result = {"error": None, "data": []}

        parser = reqparse.RequestParser()
        parser.add_argument("categories", type=list, default=[], location="json")
        parser.add_argument("states", type=list, default=[], location="json")
        parser.add_argument("genres", type=list, default=[], location="json")
        parser.add_argument("teams", type=list, default=[], location="json")
        parser.add_argument("query", type=str, default=None)
        parser.add_argument("page", type=int, default=0)
        args = parser.parse_args()

        query = utils.search_query(args["query"])
        categories = []
        genres = []
        states = []
        teams = []

        for slug in args["categories"]:
            category = DescriptorService.get_by_slug("category", slug)
            if category is not None:
                categories.append(category)
            else:
                return abort("category", "not-found")

        for slug in args["genres"]:
            genre = DescriptorService.get_by_slug("genre", slug)
            if genre is not None:
                genres.append(genre)
            else:
                return abort("genre", "not-found")

        for slug in args["states"]:
            state = DescriptorService.get_by_slug("state", slug)
            if state is not None:
                genres.append(state)
            else:
                return abort("state", "not-found")

        for slug in args["teams"]:
            team = TeamService.get_by_slug(slug)
            if team is not None:
                teams.append(team)
            else:
                return abort("team", "not-found")

        anime = AnimeService.search(
            query,
            categories,
            genres,
            states,
            teams,
            args["page"]
        )

        for anime in anime:
            result["data"].append(anime.dict())

        return result
