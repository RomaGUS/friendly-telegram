from hikka.services.permissions import PermissionService
from hikka.services.genres import GenreService
from hikka.services.func import update_document
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from hikka import utils

class NewGenre(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, default=None)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("auth", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        account = UserService.auth(args["auth"])
        if account is None:
            return abort("account", "not-found")

        if not PermissionService.check(account, "global", "admin"):
            return abort("account", "permission")

        genre_check = GenreService.get_by_slug(args["slug"])
        if genre_check is not None:
            return abort("genre", "slug-exists")

        genre = GenreService.create(args["name"], args["slug"], args["description"])
        result["data"] = {
            "description": genre.description,
            "name": genre.name,
            "slug": genre.slug
        }

        return result

class UpdateGenre(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("auth", type=str, required=True)
        parser.add_argument("params", type=dict, default={})

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        params_parser = reqparse.RequestParser()
        params_parser.add_argument("name", type=str, location=("params",))
        params_parser.add_argument("slug", type=str, location=("params",))
        params_parser.add_argument("description", type=str, location=("params",))
        params_args = params_parser.parse_args(req=args)

        account = UserService.auth(args["auth"])
        if account is None:
            return abort("account", "not-found")

        if not PermissionService.check(account, "global", "admin"):
            return abort("account", "permission")

        genre = GenreService.get_by_slug(args["slug"])
        if genre is None:
            return abort("genre", "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(params_args, keys)
        update_document(genre, update)
        genre.save()

        result["data"] = {
            "description": genre.description,
            "name": genre.name,
            "slug": genre.slug
        }

        return result
