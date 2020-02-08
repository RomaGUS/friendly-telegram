from hikka.services.permissions import PermissionsService
from werkzeug.datastructures import FileStorage
from hikka.services.files import FileService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import Response
from hikka import spaces
from hikka import utils
from PIL import Image
import secrets
import config
import shutil
import os

supported_videos = ["video/mp4"]
supported_images = ["image/jpeg", "image/png"]
supported_image_types = ["avatar", "poster"]
supported_video_types = ["release"]
image_max_size = 10 * 1024 * 1024

class UploadHelper(object):
    def __init__(self, account, upload, upload_type):
        self.name = secrets.token_hex(16)
        self.file_type = upload.filename.rsplit('.', 1)[1]
        self.spaces_name = config.spaces["name"]
        self.upload_type = upload_type
        self.account = account
        self.upload = upload

        self.file = FileService.create(self.name, self.account)
        self.folder = utils.blake2b(self.file.created.strftime("%Y/%m"), 16, config.secret).hex()
        self.fs = spaces.init_fs()

        self.spaces_dir = f"{self.spaces_name}/{self.upload_type}/{self.folder}/"
        self.tmp_dir = f"/tmp/{self.spaces_name}/{self.file.name}/"

    def upload_image(self):
        spaces_file_name = self.file.name + "." + "jpg"
        os.makedirs(self.tmp_dir)

        self.upload.save(self.tmp_dir + self.file.name + "." + self.file_type)
        pil = Image.open(self.tmp_dir + self.file.name + "." + self.file_type)
        width, height = pil.size

        if self.upload_type == "avatar":
            avatar_size = 250

            if width != height:
                return abort("image", "not-square")

            if width < avatar_size:
                return abort("image", "small-image")

            pil = pil.resize((avatar_size, avatar_size), Image.LANCZOS)

        if self.upload_type == "poster":
            max_width = 500
            if width > max_width:
                new_width = max_width
                new_height = int(new_width * height / width)
                pil = pil.resize((new_width, new_height), Image.LANCZOS)

        tmp_path = self.tmp_dir + spaces_file_name
        pil.save(tmp_path, optimize=True, quality=95)

        spaces_path = self.spaces_dir + spaces_file_name
        self.fs.put(tmp_path, spaces_path)
        self.fs.chmod(spaces_path, 'public-read')

        shutil.rmtree(self.tmp_dir)

        self.file.path = f"/{self.upload_type}/{self.folder}/{spaces_file_name}"
        self.file.uploaded = True
        self.file.save()

        return self.file

    def upload_video(self):
        spaces_file_name = self.file.name + "." + "mp4"

        os.makedirs(self.tmp_dir)
        self.upload.save(self.tmp_dir + self.file.name + "." + self.file_type)

        spaces_path = self.spaces_dir + spaces_file_name
        tmp_path = self.tmp_dir + spaces_file_name

        self.fs.put(tmp_path, spaces_path)
        self.fs.chmod(spaces_path, 'public-read')

        shutil.rmtree(self.tmp_dir)

        self.file.path = f"/{self.upload_type}/{self.folder}/{spaces_file_name}"
        self.file.uploaded = True
        self.file.save()

        return self.file

class Upload(Resource):
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("upload", type=FileStorage, location="files", default=None)
        parser.add_argument("type", type=str, required=True)
        parser.add_argument("auth", type=str, required=True)
        parser.add_argument("team", type=str)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        account = UserService.auth(args["auth"])
        if account is None:
            return abort("account", "not-found")

        if args["upload"] is None:
            return abort("file", "not-found")

        helper = UploadHelper(account, args["upload"], args["type"])

        if helper.upload.mimetype in supported_images:
            if helper.upload_type not in supported_image_types:
                return abort("file", "bad-upload-type")

            helper.upload.seek(0, os.SEEK_END)
            if helper.upload.tell() > image_max_size:
                return abort("file", "too-big")

            if helper.upload_type == "poster":
                team = TeamService.get_by_slug(args["team"])
                if team is None:
                    return abort("team", "not-found")

                if not PermissionsService.check(account, f"team-{team.slug}", "admin"):
                    return abort("account", "permission")

            helper.upload.seek(0, 0)
            data = helper.upload_image()

        elif helper.upload.mimetype in supported_videos:
            if helper.upload_type not in supported_video_types:
                return abort("file", "bad-upload-type")

            if helper.upload_type == "release":
                team = TeamService.get_by_slug(args["team"])
                if team is None:
                    return abort("team", "not-found")

                if not PermissionsService.check(account, f"team-{team.slug}", "admin"):
                    return abort("account", "permission")

            data = helper.upload_video()

        else:
            return abort("file", "bad-mime-type")

        if type(data) is Response:
            return data

        result["data"]["path"] = config.cdn + data.path
        result["data"]["name"] = data.name

        return result
