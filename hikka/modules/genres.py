from hikka.services.permissions import PermissionsService
from hikka.services.genres import GenresService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka import utils

class NewGenre(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, default=None, required=True)
        parser.add_argument("name", type=str, default=None, required=True)
        parser.add_argument("slug", type=str, default=None, required=True)
        parser.add_argument("auth", type=str, default=None, required=True)
        args = parser.parse_args()

        result = {
            "error": utils.errors["account-not-found"],
            "data": {}
        }

        account = UserService.auth(args["auth"])

        if account is not None:
            result["error"] = utils.errors["account-permission"]

            if PermissionsService.check(account, "global", "admin"):
                result["error"] = utils.errors["genre-slug-exists"]
                genre_check = GenresService.get_by_slug(args["slug"])

                if genre_check is None:
                    genre = GenresService.create(args["name"], args["slug"], args["description"])

                    result["error"] = None
                    result["data"] = {
                        "description": genre.description,
                        "name": genre.name,
                        "slug": genre.slug
                    }

        return result
