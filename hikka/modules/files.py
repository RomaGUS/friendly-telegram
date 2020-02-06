from werkzeug.datastructures import FileStorage
from hikka.services.files import FileService
from hikka.services.users import UserService
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from hikka import spaces
from hikka import utils
from PIL import Image
import secrets
import config
import shutil
import os

supported_images = ["image/jpeg", "image/png"]
supported_images_types = ["avatar"]

class Upload(Resource):
    def post(self):
        result = {"error": None, "data": {}}
        spaces_name = config.spaces["name"]

        parser = reqparse.RequestParser()
        parser.add_argument("upload", type=FileStorage, location="files", default=None)
        parser.add_argument("type", type=str, required=True)
        parser.add_argument("auth", type=str, required=True)

        try:
            args = parser.parse_args()
        except Exception:
            return abort("general", "missing-field")

        account = UserService.auth(args["auth"])
        if account is None:
            return abort("account", "not-found")

        upload_type = args["type"]
        upload = args["upload"]

        if args["upload"] is None:
            return abort("file", "not-found")

        name = secrets.token_hex(16)
        file = FileService.create(name, account)
        folder = utils.blake2b(file.created.strftime("%Y/%m"), 16, config.secret).hex()
        fs = spaces.init_fs()

        if upload.mimetype in supported_images:
            if upload_type not in supported_images_types:
                return abort("file", "bad-upload-type")

            result["error"] = None

            file_type = upload.filename.rsplit('.', 1)[1]
            tmp_file_name = file.name + "." + file_type
            spaces_file_name = file.name + "." + "jpg"

            spaces_dir = f"{spaces_name}/{upload_type}/{folder}/"
            tmp_dir = f"/tmp/{spaces_name}/{file.name}/"

            os.makedirs(tmp_dir)
            upload.save(tmp_dir + tmp_file_name)
            pil = Image.open(tmp_dir + tmp_file_name)

            if upload_type == "avatar":
                size = pil.size
                if size[0] != size[1]:
                    return abort("image", "not-square")

            if upload_type == "avatar":
                max_size = 250
                pil = pil.resize((max_size, max_size), Image.LANCZOS)

            tmp_path = tmp_dir + spaces_file_name
            pil.save(tmp_path, optimize=True, quality=95)

            spaces_path = spaces_dir + spaces_file_name
            fs.put(tmp_path, spaces_path)
            fs.chmod(spaces_path, 'public-read')

            shutil.rmtree(tmp_dir)

            file.path = f"/{upload_type}/{folder}/{spaces_file_name}"
            file.uploaded = True
            file.save()

            result["data"]["path"] = config.cdn + file.path
            result["data"]["name"] = file.name

        return result
