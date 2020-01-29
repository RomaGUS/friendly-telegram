from hikka.services.permissions import PermissionsService
from hikka.services.types import ReleaseTypesService
from hikka.services.releases import ReleasesService
from hikka.services.genres import GenresService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka import utils

class NewRelease(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, default=None, required=True)
        parser.add_argument("name", type=str, default=None, required=True)
        parser.add_argument("slug", type=str, default=None, required=True)
        parser.add_argument("team", type=str, default=None, required=True)
        parser.add_argument("type", type=str, default=None, required=True)
        parser.add_argument("auth", type=str, default=None, required=True)
        parser.add_argument("genres", type=list, default=[])
        args = parser.parse_args()

        result = {
            "error": utils.errors["account-not-found"],
            "data": {}
        }

        account = UserService.auth(args["auth"])

        if account is not None:
            result["error"] = utils.errors["team-not-found"]
            team = TeamService.get_by_slug(args["team"])

            if team is not None:
                result["error"] = utils.errors["account-permission"]

                if PermissionsService.check(account, f"team-{team.slug}", "admin"):
                    result["error"] = None

                    release = ReleasesService.get_by_slug(args["slug"])
                    if release is not None:
                        result["error"] = utils.errors["release-slug-exists"]

                    rtype = ReleaseTypesService.get_by_slug(args["type"])
                    if rtype is None:
                        result["error"] = utils.errors["type-not-found"]

                    if args["name"] is None:
                        result["error"] = utils.errors["missing-field"]

                    if args["description"] is None:
                        result["error"] = utils.errors["missing-field"]

                    genres = []
                    for slug in args["genres"]:
                        genre = GenresService.get_by_slug(slug)
                        if genre is not None:
                            genres.append(genre)

                        else:
                            result["error"] = utils.errors["genre-not-found"]
                            break

                    if result["error"] is None:
                        release = ReleasesService.create(
                            args["name"],
                            args["slug"],
                            args["description"],
                            rtype,
                            genres,
                            [team]
                        )

                        result["data"] = {
                            "name": release.name,
                            "description": release.description,
                            "type": release.rtype.slug,
                            "slug": release.slug
                        }

        return result
