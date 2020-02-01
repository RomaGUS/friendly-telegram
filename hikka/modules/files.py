from flask_restful import Resource
from flask import request
from hikka import spaces
from hikka import errors
from PIL import Image
import secrets
import shutil
import os

supported_images = ["image/jpeg", "image/png"]

def upload_avatar(result, file):
    result["error"] = errors.get("file", "bad-mime")
    fs = spaces.init_fs()
    max_size = 250

    if file.mimetype in supported_images:
        result["error"] = None

        file_type = file.filename.rsplit('.', 1)[1]
        save_type = "jpg"

        file_token = secrets.token_hex(16)
        file_name = f"hikka_{file_token}"

        spaces_dir = f"hikka/volbil/"
        tmp_dir = f"/tmp/hikka/{file_token}/"

        result["data"]["type"] = file_type
        result["data"]["name"] = file_name

        os.makedirs(tmp_dir)
        file.save(tmp_dir + file_name + "." + file_type)

        spaces_path = spaces_dir + file_name + "." + save_type
        tmp_path = tmp_dir + file_name + "." + save_type

        pil = Image.open(tmp_dir + file_name + "." + file_type)

        size = pil.size

        if size[0] != size[1]:
            pass

        pil = pil.resize((max_size, max_size), Image.LANCZOS)
        pil.save(tmp_path, optimize=True, quality=95)

        fs.put(tmp_path, spaces_path)
        fs.chmod(spaces_path, 'public-read')

        shutil.rmtree(tmp_dir)

    return result

class Upload(Resource):
    def post(self):
        result = {
            "error": errors.get("file", "not-found"),
            "data": {}
        }

        if "upload" in request.files:
            result["error"] = errors.get("file", "bad-upload-type")
            upload_type = "avatar"

            if upload_type == "avatar":
                upload_avatar(result, request.files["upload"])

        return result
