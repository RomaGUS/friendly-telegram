from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from werkzeug.datastructures import FileStorage
from hikka.services.anime import AnimeService
from hikka.services.files import FileService
from hikka.tools.parser import RequestParser
from hikka.tools.upload import UploadHelper
from flask_restful import Resource
from flask import request, session
from hikka.tools import helpers
from hikka.errors import abort
from flask import Response
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
        parser.add_argument("state", type=helpers.state, required=True)
        parser.add_argument("team", type=helpers.team, required=True)
        parser.add_argument("season", type=int, choices=range(1, 5))
        parser.add_argument("title", type=dict, required=True)
        parser.add_argument("year", type=int, required=True)
        parser.add_argument("external", type=dict)
        parser.add_argument("total", type=int)
        args = parser.parse_args()

        title_parser = RequestParser()
        title_parser.add_argument("ua", type=helpers.string, location="title", required=True)
        title_parser.add_argument("jp", type=helpers.string, location="title")
        title_args = title_parser.parse_args(req=args)

        external_parser = RequestParser()
        external_parser.add_argument("myanimelist", type=int, location="external")
        external_parser.add_argument("toloka", type=int, location="external")
        external_args = external_parser.parse_args(req=args)

        title = AnimeService.get_title(title_args["ua"], title_args["jp"])
        slug = utils.create_slug(title_args["ua"])
        team = args["team"]

        anime = AnimeService.create(
            title, args["description"],
            args["category"], args["state"],
            slug
        )

        for alias in args["aliases"]:
            if type(alias) is not str:
                return abort("general", "alias-invalid-type")

        if request.account not in team.members:
            return abort("account", "not-team-member")

        anime.genres = []
        for slug in args["genres"]:
            genre = helpers.genre(slug)
            anime.genres.append(genre)

        anime.franchises = []
        for slug in args["franchises"]:
            franchise = helpers.franchise(slug)
            anime.franchises.append(franchise)

        fields = ["aliases", "year", "total"]
        for field in fields:
            anime[field] = args[field]

        fields = ["subtitles", "voiceover"]
        for field in fields:
            anime[field] = []
            for username in args[field]:
                account = helpers.account(username)
                anime[field].append(account)

        search = utils.create_search(anime.title.ua, anime.title.jp, anime.aliases)
        external = AnimeService.get_external(external_args["myanimelist"], external_args["toloka"])

        anime.external = external
        anime.search = search
        anime.teams = [team]

        if anime.external.myanimelist:
            anime.rating = utils.rating(anime.external.myanimelist)
            anime.save()

        result["data"] = anime.dict()
        anime.save()

        return result

class EditAnime(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("params", type=dict, default={}, location="json")
        parser.add_argument("slug", type=helpers.anime, required=True)
        args = parser.parse_args()

        params_parser = RequestParser()
        params_parser.add_argument("season", type=int, choices=range(1, 5), location="params")
        params_parser.add_argument("description", type=helpers.string, location="params")
        params_parser.add_argument("category", type=helpers.category, location="params")
        params_parser.add_argument("state", type=helpers.state, location="params")
        params_parser.add_argument("franchises", type=list, location="params")
        params_parser.add_argument("subtitles", type=list, location="params")
        params_parser.add_argument("voiceover", type=list, location="params")
        params_parser.add_argument("external", type=dict, location="params")
        params_parser.add_argument("selected", type=bool, location="params")
        params_parser.add_argument("aliases", type=list, location="params")
        params_parser.add_argument("genres", type=list, location="params")
        params_parser.add_argument("title", type=dict, location="params")
        params_parser.add_argument("total", type=int, location="params")
        params_parser.add_argument("year", type=int, location="params")
        params_args = params_parser.parse_args(req=args)

        title_parser = RequestParser()
        title_parser.add_argument("jp", type=str, location="title")
        title_parser.add_argument("ua", type=str, location="title")
        title_args = title_parser.parse_args(req=params_args)

        external_parser = RequestParser()
        external_parser.add_argument("myanimelist", type=int, location="external")
        external_parser.add_argument("toloka", type=int, location="external")
        external_args = external_parser.parse_args(req=params_args)

        anime = args["slug"]

        if params_args["aliases"]:
            for alias in args["aliases"]:
                if type(alias) is not str:
                    return abort("general", "alias-invalid-type")

        if params_args["genres"]:
            anime.genres = []
            for slug in params_args["genres"]:
                genre = helpers.genre(slug)
                anime.genres.append(genre)

        if params_args["franchises"]:
            anime.franchises = []
            for slug in params_args["franchises"]:
                franchise = helpers.franchise(slug)
                anime.franchises.append(franchise)

        fields = ["category", "description", "state", "year", "total", "selected", "aliases", "season"]
        for field in fields:
            if params_args[field]:
                anime[field] = params_args[field]

        fields = ["subtitles", "voiceover"]
        for field in fields:
            if params_args[field]:
                anime[field] = []
                for username in params_args[field]:
                    account = helpers.account(username)
                    anime[field].append(account)

        fields = ["jp", "ua"]
        for field in fields:
            if title_args[field]:
                anime.title[field] = title_args[field]

        if params_args["external"]:
            if external_args["myanimelist"]:
                anime.external.myanimelist = external_args["myanimelist"]
                anime.rating = utils.rating(anime.external.myanimelist)

            if external_args["toloka"]:
                anime.external.toloka = external_args["toloka"]

        if PermissionService.check(request.account, "global", "admin"):
            if params_args["selected"]:
                anime["selected"] = params_args["selected"]

        anime.search = utils.create_search(anime.title.ua, anime.title.jp, anime.aliases)
        anime.save()

        result["data"] = anime.dict()
        return result

class AnimeUpload(Resource):
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

        if args["file"]:
            helper = UploadHelper(request.account, args["file"], args["type"])
            data = helper.upload_image()

            if type(data) is Response:
                return data

            if anime[args["type"]]:
                FileService.destroy(anime[args["type"]])

            anime[args["type"]] = data
            anime.save()

        result["data"] = anime.dict()
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
        year_parser.add_argument("min", type=int, location="year")
        year_parser.add_argument("max", type=int, location="year")
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
            states.append(state)

        for slug in args["teams"]:
            team = helpers.team(slug)
            teams.append(team)

        anime = AnimeService.search(
            query, year_args, categories,
            genres, franchises, states,
            teams, False, args["page"]
        )

        for item in anime:
            result["data"].append(item.dict())

        return result

class GetAnime(Resource):
    @auth_required
    def get(self, slug):
        result = {"error": None, "data": {}}

        anime = helpers.anime(slug)
        result["data"] = anime.dict(True)

        if str(anime.id) not in session:
            session[str(anime.id)] = []
            anime.views += 1
            anime.save()

        return result

class Selected(Resource):
    @auth_required
    def get(self):
        result = {"error": None, "data": []}

        anime = AnimeService.selected()
        for item in anime:
            result["data"].append(item.dict())

        return result
