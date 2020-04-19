from hikka.decorators import auth_required, permission_required
from hikka.services.anime import AnimeService
from hikka.tools.parser import RequestParser
from hikka.services.files import FileService
from flask import request, Blueprint
from hikka.tools import helpers
from hikka.errors import abort

blueprint = Blueprint("episodes", __name__)

@blueprint.route("/episodes/add", methods=["POST"])
@auth_required
@permission_required("global", "publishing")
def add_episode():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("position", type=helpers.position, required=True)
    parser.argument("slug", type=helpers.anime, required=True)
    parser.argument("name", type=str)
    args = parser.parse()

    anime = args["slug"]
    helpers.is_member(request.account, anime.teams)

    position = AnimeService.position(anime, args["position"])
    if position is not None:
        return abort("episode", "position-exists")

    episode = AnimeService.get_episode(args["name"], args["position"])
    AnimeService.add_episode(anime, episode)
    result["data"] = anime.dict(True)

    return result

@blueprint.route("/episodes/update", methods=["POST"])
@auth_required
@permission_required("global", "publishing")
def update_episode():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("position", type=helpers.position, required=True)
    parser.argument("slug", type=helpers.anime, required=True)
    parser.argument("params", type=dict, default={})
    args = parser.parse()

    params_parser = RequestParser()
    params_parser.argument("name", type=helpers.string, location="params")
    params_args = params_parser.parse(req=args)

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

@blueprint.route("/episodes/delete", methods=["POST"])
@auth_required
@permission_required("global", "publishing")
def delete_episode():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("position", type=helpers.position, required=True)
    parser.argument("slug", type=helpers.anime, required=True)
    args = parser.parse()

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
