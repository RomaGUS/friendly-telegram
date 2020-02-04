from hikka.services.files import FileService
from hikka.services.users import UserService
from flask_restful import Resource
from hikka.errors import abort
from flask import request
from hikka import spaces
from hikka import utils
from PIL import Image
import secrets
import config
import shutil
import os

supported_images = ["image/jpeg", "image/png"]

class Upload(Resource):
    def post(self):
        result = {"error": None, "data": {}}
        fs = spaces.init_fs()

        if "upload" not in request.files:
            return abort("file", "not-found")

        upload_type = "avatar"
        name = secrets.token_hex(16)
        account = UserService.get_by_username("volbil")
        file = FileService.create(name, account)
        folder = utils.blake2b(file.created.strftime("%Y/%m"), 16, config.secret).hex()
        spaces_name = config.spaces["name"]

        if upload_type == "avatar":
            upload = request.files["upload"]
            max_size = 250

            if upload.mimetype in supported_images:
                result["error"] = None

                file_type = upload.filename.rsplit('.', 1)[1]
                save_type = "jpg"

                spaces_dir = f"{spaces_name}/{upload_type}/{folder}/"
                tmp_dir = f"/tmp/{spaces_name}/{file.name}/"

                os.makedirs(tmp_dir)
                upload.save(tmp_dir + file.name + "." + file_type)

                spaces_path = spaces_dir + file.name + "." + save_type
                tmp_path = tmp_dir + file.name + "." + save_type

                pil = Image.open(tmp_dir + file.name + "." + file_type)

                size = pil.size

                if size[0] != size[1]:
                    return abort("image", "not-square")

                pil = pil.resize((max_size, max_size), Image.LANCZOS)
                pil.save(tmp_path, optimize=True, quality=95)

                fs.put(tmp_path, spaces_path)
                fs.chmod(spaces_path, 'public-read')

                shutil.rmtree(tmp_dir)

                file.uploaded = True
                file.path = f"/{upload_type}/{folder}/{file.name}.{save_type}"
                file.save()

                result["data"]["path"] = config.cdn + file.path
                result["data"]["name"] = file.name

        else:
            return abort("file", "bad-upload-type")

        return result
