from hikka.decorators import auth_required, permission_required
from hikka.services.anime import AnimeService
from hikka.tools.parser import RequestParser
from hikka.services.files import FileService
from flask import request, Blueprint
from hikka.tools import helpers
from hikka.errors import abort

blueprint = Blueprint("episodes", __name__)

@blueprint.route("/episodes/manage", methods=["POST"])
@auth_required
@permission_required("global", "publishing")
def add_episode():
    result = {"error": None, "data": {}}

    parser = RequestParser()
    parser.argument("opening", type=helpers.opening, location="json")
    parser.argument("position", type=helpers.position, required=True)
    parser.argument("slug", type=helpers.anime, required=True)
    parser.argument("ending", type=int)
    parser.argument("name", type=str)
    args = parser.parse()

    anime = args["slug"]
    helpers.is_member(request.account, anime.teams)

    index = AnimeService.position_index(anime, args["position"])
    if index is None:
        episode = AnimeService.get_episode(args["position"])
        AnimeService.add_episode(anime, episode)
    else:
        episode = anime.episodes[index]

    fields = ["name", "opening", "ending"]
    for field in fields:
        if args[field]:
            episode[field] = args[field]

    anime.save()
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

    index = AnimeService.position_index(anime, args["position"])
    if index is None:
        return abort("episode", "not-found")

    FileService.destroy(anime.episodes[index].video)
    FileService.destroy(anime.episodes[index].thumbnail)
    AnimeService.remove_episode(anime, anime.episodes[index])

    result["data"] = anime.dict(True)
    return result
