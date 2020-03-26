from hikka.decorators import auth_required, permission_required
from werkzeug.datastructures import FileStorage
from hikka.services.anime import AnimeService
from hikka.tools.parser import RequestParser
from hikka.services.files import FileService
from hikka.tools.upload import UploadHelper
from flask_restful import Resource
from hikka.tools import helpers
from hikka.errors import abort
from flask import Response
from flask import request

class AddEpisode(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("video", type=FileStorage, location="files")
        parser.add_argument("slug", type=helpers.anime, required=True)
        parser.add_argument("position", type=int, required=True)
        parser.add_argument("name", type=str, default=None)
        args = parser.parse_args()

        if args["position"] < 0:
            return abort("general", "out-of-range")

        anime = args["slug"]

        if request.account not in anime.team.members:
            return abort("account", "not-team-member")

        episode = AnimeService.find_position(anime, args["position"])
        if episode is not None:
            return abort("episode", "position-exists")

        if args["video"] is None:
            return abort("file", "not-found")

        helper = UploadHelper(request.account, args["video"], "video")
        data = helper.upload_video()

        if type(data) is Response:
            return data

        video = data
        episode = AnimeService.get_episode(args["name"], args["position"], video)
        AnimeService.add_episode(anime, episode)

        result["data"] = anime.dict(True)
        return result

class UpdateEpisode(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("video", type=FileStorage, location="files")
        parser.add_argument("slug", type=helpers.anime, required=True)
        parser.add_argument("position", type=int, required=True)
        parser.add_argument("params", type=dict, default={})
        args = parser.parse_args()

        anime = args["slug"]

        if request.account not in anime.team.members:
            return abort("account", "not-team-member")

        episode = AnimeService.find_position(anime, args["position"])
        if episode is None:
            return abort("episode", "not-found")

        video = episode.video
        if args["video"] is not None:
            helper = UploadHelper(request.account, args["video"], "video")
            data = helper.upload_video()

            if type(data) is Response:
                return data

            FileService.destroy(episode.video)
            video = data

        name = episode.name
        if "name" in args["params"]:
            name = args["params"]["name"]

        position = episode.position
        if "position" in args["params"]:
            if args["position"] < 0:
                return abort("general", "out-of-range")

            episode_check = AnimeService.find_position(anime, args["position"])
            if episode_check is not None:
                return abort("episode", "position-exists")

            position = args["params"]["position"]

        AnimeService.remove_episode(anime, episode)
        episode = AnimeService.get_episode(name, position, video)
        AnimeService.add_episode(anime, episode)

        result["data"] = anime.dict(True)
        return result

class DeleteEpisode(Resource):
    @auth_required
    @permission_required("global", "publishing")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.add_argument("slug", type=helpers.anime, required=True)
        parser.add_argument("position", type=int, required=True)
        args = parser.parse_args()

        anime = args["slug"]

        if request.account not in anime.team.members:
            return abort("account", "not-team-member")

        episode = AnimeService.find_position(anime, args["position"])
        if episode is None:
            return abort("episode", "not-found")

        FileService.destroy(episode.video)
        AnimeService.remove_episode(anime, episode)

        result["data"] = anime.dict(True)
        return result
