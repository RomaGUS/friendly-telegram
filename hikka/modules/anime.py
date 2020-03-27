from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from werkzeug.datastructures import FileStorage
from hikka.services.anime import AnimeService
from hikka.services.files import FileService
from hikka.tools.parser import RequestParser
from hikka.tools.upload import UploadHelper
from flask_restful import Resource
from hikka.tools import helpers
from hikka.errors import abort
from flask import Response
from flask import request
from hikka import utils

class NewAnime(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("franchises", type=list, default=[], location="json")
        parser.add_argument("subtitles", type=list, default=[], location="json")
        parser.add_argument("voiceover", type=list, default=[], location="json")
        parser.add_argument("aliases", type=list, default=[], location="json")
        parser.add_argument("genres", type=list, default=[], location="json")
        parser.add_argument("category", type=helpers.category, required=True)
        parser.add_argument("description", type=helpers.string, required=True)
        parser.add_argument("state", type=helpers.state, default=None)
        parser.add_argument("team", type=helpers.team, required=True)
        parser.add_argument("title", type=dict, required=True)
        parser.add_argument("year", type=int, required=True)
        parser.add_argument("total", type=int, default=None)
        parser.add_argument("external", type=dict)
        args = parser.parse_args()

        title_parser = RequestParser()
        title_parser.add_argument("jp", type=str, default=None, location=("title",))
        title_parser.add_argument("ua", type=str, location=("title",))
        title_args = title_parser.parse_args(req=args)

        external_parser = RequestParser()
        external_parser.add_argument("mal", type=int, default=None, location=("external"))
        external_args = external_parser.parse_args(req=args)

        for alias in args["aliases"]:
            if type(alias) is not str:
                return abort("general", "alias-invalid-type")

        team = args["team"]

        if request.account not in team.members:
            return abort("account", "not-team-member")

        if not PermissionService.check(request.account, "global", "publishing"):
            return abort("account", "permission")

        genres = []
        for slug in args["genres"]:
            genre = helpers.genre(slug)
            genres.append(genre)

        franchises = []
        for slug in args["franchises"]:
            franchise = helpers.franchise(slug)
            franchises.append(franchise)

        subtitles = []
        for username in args["subtitles"]:
            subtitles_account = helpers.account(username)
            subtitles.append(subtitles_account)

        voiceover = []
        for username in args["voiceover"]:
            voiceover_account = helpers.account(username)
            voiceover.append(voiceover_account)

        title = AnimeService.get_title(title_args["ua"], title_args["jp"])
        search = utils.create_search(title_args["ua"], title_args["jp"], args["aliases"])
        external = AnimeService.get_external(external_args["mal"])
        slug = utils.create_slug(title_args["ua"])

        anime = AnimeService.create(
            title,
            slug,
            args["description"],
            args["year"],
            args["total"],
            search,
            args["category"],
            args["state"],
            external,
            genres,
            franchises,
            [team],
            subtitles,
            voiceover,
            args["aliases"]
        )

        # Get rating from MyAnimeList
        if anime.external.mal is not None:
            anime.rating = utils.rating(anime.external.mal)
            anime.save()

        result["data"] = anime.dict()
        return result

class Upload(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def put(self):
        result = {"error": None, "data": []}
        choices = ("poster", "banner")

        parser = RequestParser()
        parser.add_argument("file", type=FileStorage, location="files")
        parser.add_argument("slug", type=helpers.anime, required=True)
        parser.add_argument("type", type=str, choices=choices)
        args = parser.parse_args()

        anime = args["slug"]

        if args["file"] is not None:
            helper = UploadHelper(request.account, args["file"], args["type"])
            data = helper.upload_image()

            if type(data) is Response:
                return data

            if anime[args["type"]] is not None:
                FileService.destroy(anime[args["type"]])

            anime[args["type"]] = data
            anime.save()

        result["data"] = anime.dict()
        return result

class GetAnime(Resource):
    @auth_required
    def get(self, slug):
        result = {"error": None, "data": {}}

        anime = helpers.anime(slug)
        result["data"] = anime.dict(True)

        return result

class Search(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": []}

        parser = RequestParser()
        parser.add_argument("franchises", type=list, default=[], location="json")
        parser.add_argument("categories", type=list, default=[], location="json")
        parser.add_argument("states", type=list, default=[], location="json")
        parser.add_argument("genres", type=list, default=[], location="json")
        parser.add_argument("teams", type=list, default=[], location="json")
        parser.add_argument("query", type=str, default="")
        parser.add_argument("page", type=int, default=0)
        parser.add_argument("year", type=dict)
        args = parser.parse_args()

        year_parser = RequestParser()
        year_parser.add_argument("min", type=int, default=None, location=("year",))
        year_parser.add_argument("max", type=int, default=None, location=("year",))
        year_args = year_parser.parse_args(req=args)

        query = utils.search_query(args["query"])
        categories = []
        franchises = []
        genres = []
        states = []
        teams = []

        for slug in args["categories"]:
            category = helpers.category(slug)
            categories.append(category)

        for slug in args["genres"]:
            genre = helpers.genre(slug)
            genres.append(genre)

        for slug in args["franchises"]:
            franchise = helpers.franchise(slug)
            franchises.append(franchise)

        for slug in args["states"]:
            state = helpers.state(slug)
            genres.append(state)

        for slug in args["teams"]:
            team = helpers.team(slug)
            teams.append(team)

        anime = AnimeService.search(
            query,
            year_args,
            categories,
            genres,
            franchises,
            states,
            teams,
            args["page"]
        )

        for anime in anime:
            result["data"].append(anime.dict())

        return result
