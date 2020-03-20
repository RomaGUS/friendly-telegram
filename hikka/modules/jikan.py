from flask_restful import Resource
from flask_restful import reqparse
from jikanpy import Jikan

class JikanSearch(Resource):
    def post(self):
        result = {"error": None, "data": []}

        parser = reqparse.RequestParser()
        parser.add_argument("query", type=str, default="")
        parser.add_argument("page", type=int, default=1)
        args = parser.parse_args()

        jikan = Jikan()

        return jikan.search("anime", args["query"], page=args["page"])
