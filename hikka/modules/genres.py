from hikka.decorators import auth_required, permission_required
from hikka.services.func import update_document
from hikka.services.genres import GenreService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from hikka import utils

class NewGenre(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str, default=None)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

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
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("params", type=dict, default={})

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        genre = GenreService.get_by_slug(args["slug"])
        if genre is None:
            return abort("genre", "not-found")

        keys = ["name", "slug", "description"]
        update = utils.filter_dict(args["params"], keys)
        update_document(genre, update)

        try:
            genre.save()
        except Exception:
            return abort("general", "empty-required")

        result["data"] = {
            "description": genre.description,
            "name": genre.name,
            "slug": genre.slug
        }

        return result
