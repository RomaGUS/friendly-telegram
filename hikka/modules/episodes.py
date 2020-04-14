from hikka.decorators import auth_required, permission_required
from werkzeug.datastructures import FileStorage
from hikka.services.anime import AnimeService
from hikka.tools.parser import RequestParser
from hikka.services.files import FileService
from hikka.tools.upload import UploadHelper
from flask_restful import Resource
from hikka.tools import helpers
from hikka.errors import abort
from flask import request

class AddEpisode(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("position", type=helpers.position, required=True)
        parser.add_argument("slug", type=helpers.anime, required=True)
        parser.add_argument("name", type=str)
        args = parser.parse_args()

        anime = args["slug"]
        helpers.is_member(request.account, anime.teams)

        position = AnimeService.position(anime, args["position"])
        if position is not None:
            return abort("episode", "position-exists")

        episode = AnimeService.get_episode(args["name"], args["position"])
        AnimeService.add_episode(anime, episode)
        result["data"] = anime.dict(True)

        return result

class UpdateEpisode(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("position", type=helpers.position, required=True)
        parser.add_argument("slug", type=helpers.anime, required=True)
        parser.add_argument("params", type=dict, default={})
        args = parser.parse_args()

        params_parser = RequestParser()
        params_parser.add_argument("name", type=helpers.string, location="params")
        params_args = params_parser.parse_args(req=args)

        anime = args["slug"]
        helpers.is_member(request.account, anime.teams)

        position = AnimeService.position(anime, args["position"])
        if position is None:
            return abort("episode", "not-found")

        fields = ["name"]
        for field in fields:
            if params_args[field]:
                anime.episodes[position][field] = params_args[field]

        result["data"] = anime.dict(True)
        return result

class DeleteEpisode(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("position", type=helpers.position, required=True)
        parser.add_argument("slug", type=helpers.anime, required=True)
        args = parser.parse_args()

        anime = args["slug"]
        helpers.is_member(request.account, anime.teams)

        position = AnimeService.position(anime, args["position"])
        if position is None:
            return abort("episode", "not-found")

        FileService.destroy(anime.episodes[position].video)
        FileService.destroy(anime.episodes[position].thumbnail)
        AnimeService.remove_episode(anime, anime.episodes[position])

        result["data"] = anime.dict(True)
        return result

class EpisodeUpload(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def put(self):
        result = {"error": None, "data": []}
        choices = ("thumbnail", "video")

        parser = RequestParser()
        parser.add_argument("position", type=helpers.position, required=True)
        parser.add_argument("file", type=FileStorage, location="files")
        parser.add_argument("slug", type=helpers.anime, required=True)
        parser.add_argument("type", type=str, choices=choices)
        args = parser.parse_args()

        anime = args["slug"]
        helpers.is_member(request.account, anime.teams)

        episode = AnimeService.position(anime, args["position"])
        if episode is None:
            return abort("episode", "not-found")

        if args["file"]:
            helper = UploadHelper(request.account, args["file"], args["type"])

            if args["type"] == "thumbnail":
                data = helper.upload_image()
            else:
                data = helper.upload_video()

            if episode[args["type"]]:
                FileService.destroy(episode[args["type"]])

            episode[args["type"]] = data
            anime.save()

        result["data"] = anime.dict()
        return result
