from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from werkzeug.datastructures import FileStorage
from hikka.services.anime import AnimeService
from hikka.services.files import FileService
from hikka.tools.parser import RequestParser
from hikka.tools.upload import UploadHelper
from flask.views import MethodView
from hikka.tools import helpers
from flask import request
import shutil
import os

class ManagePermissions(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("action", type=str, required=True, choices=("add", "remove"))
        parser.argument("account", type=helpers.account, required=True)
        parser.argument("scope", type=str, required=True)
        parser.argument("name", type=str, required=True)
        args = parser.parse()

        account = args["account"]

        if args["action"] == "add":
            PermissionService.add(account, args["scope"], args["name"])

        elif args["action"] == "remove":
            PermissionService.remove(account, args["scope"], args["name"])

        result["data"] = account.list_permissions()

        return result

class UserPermissions(MethodView):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = RequestParser()
        parser.argument("account", type=helpers.account, required=True)
        args = parser.parse()

        account = args["account"]
        result["data"] = account.list_permissions()

        return result

class StaticData(MethodView):
    def get(self):
        result = {"error": None, "data": {}}
        result["data"]["years"] = AnimeService.years()
        return result["data"]["static"]

class SystemUpload(MethodView):
    @auth_required
    def put(self):
        result = {"error": None, "data": {}}
        choices = ("poster", "banner")

        parser = RequestParser()
        parser.argument("type", type=str, choices=choices, required=True)
        parser.argument("file", type=FileStorage, location="files")
        # parser.argument("slug", type=helpers.anime, required=True)
        parser.argument("uuid", type=helpers.uuid, required=True)
        # parser.argument("link", type=helpers.image_link)
        args = parser.parse()

        folder = request.account.username
        upload_type = args["type"]
        uuid = args["uuid"]

        tmp_dir = f"/tmp/hikka/{folder}/{upload_type}/"
        uuid_dir = os.path.join(tmp_dir, uuid)

        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)

        tmp_ls = os.listdir(tmp_dir)

        if uuid not in tmp_ls:
            shutil.rmtree(tmp_dir)
            os.makedirs(tmp_dir)
            os.mkdir(uuid_dir)

        result["data"]["ls"] = os.listdir(tmp_dir)

        return result

        # anime = args["slug"]
        # helpers.is_member(request.account, anime.teams)

        # upload_type = None
        # upload = None

        # fields = ["file", "link"]
        # for field in fields:
        #     if args[field]:
        #         upload_type = field
        #         upload = args[field]

        # if upload_type:
        #     helper = UploadHelper(request.account, upload, upload_type, args["type"])
        #     data = helper.upload_image()

        #     if anime[args["type"]]:
        #         FileService.destroy(anime[args["type"]])

        #     anime[args["type"]] = data
        #     anime.save()

        # result["data"] = anime.dict()
        # return result
