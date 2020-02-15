from hikka.services.permissions import PermissionService
from hikka.services.releases import ReleaseService
from werkzeug.datastructures import FileStorage
from hikka.services.teams import TeamService
from hikka.services.files import FileService
from hikka.decorators import auth_required
from hikka.upload import UploadHelper
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import Response
from flask import request

class AddEpisode(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("video", type=FileStorage, location="files")
        parser.add_argument("position", type=int, required=True)
        parser.add_argument("team", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("name", type=str, default=None)
        args = parser.parse_args()

        if args["position"] < 0:
            return abort("general", "out-of-range")

        team = TeamService.get_by_slug(args["team"])
        if team is None:
            return abort("team", "not-found")

        if not PermissionService.check(request.account, f"team-{team.slug}", "admin"):
            return abort("account", "permission")

        release = ReleaseService.get_by_slug(args["slug"])
        if release is None:
            return abort("release", "not-found")

        episode = ReleaseService.find_position(release, args["position"])
        if episode is not None:
            return abort("episodes", "position-exists")

        if args["video"] is None:
            return abort("file", "not-found")

        helper = UploadHelper(request.account, args["video"], "video")
        data = helper.upload_video()

        if type(data) is Response:
            return data

        video = data
        episode = ReleaseService.get_episode(args["name"], args["position"], video)
        ReleaseService.add_episode(release, episode)

        result["data"] = release.dict(True)
        return result

class UpdateEpisode(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("video", type=FileStorage, location="files")
        parser.add_argument("position", type=int, required=True)
        parser.add_argument("team", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("params", type=dict, default={})
        args = parser.parse_args()

        team = TeamService.get_by_slug(args["team"])
        if team is None:
            return abort("team", "not-found")

        if not PermissionService.check(request.account, f"team-{team.slug}", "admin"):
            return abort("account", "permission")

        release = ReleaseService.get_by_slug(args["slug"])
        if release is None:
            return abort("release", "not-found")

        episode = ReleaseService.find_position(release, args["position"])
        if episode is None:
            return abort("episodes", "not-found")

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

            episode_check = ReleaseService.find_position(release, args["position"])
            if episode_check is not None:
                return abort("episodes", "position-exists")

            position = args["params"]["position"]

        ReleaseService.remove_episode(release, episode)
        episode = ReleaseService.get_episode(name, position, video)
        ReleaseService.add_episode(release, episode)

        result["data"] = release.dict(True)
        return result

class DeleteEpisode(Resource):
    @auth_required
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("position", type=int, required=True)
        parser.add_argument("team", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        team = TeamService.get_by_slug(args["team"])
        if team is None:
            return abort("team", "not-found")

        if not PermissionService.check(request.account, f"team-{team.slug}", "admin"):
            return abort("account", "permission")

        release = ReleaseService.get_by_slug(args["slug"])
        if release is None:
            return abort("release", "not-found")

        episode = ReleaseService.find_position(release, args["position"])
        if episode is None:
            return abort("episodes", "not-found")

        FileService.destroy(episode.video)
        ReleaseService.remove_episode(release, episode)

        result["data"] = release.dict(True)
        return result
