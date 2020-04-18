from werkzeug.datastructures import FileStorage
from hikka.services.files import FileService
from flask import abort as flask_abort
from hikka.tools import storage
from hikka.errors import abort
from hikka import utils
from io import BytesIO
from PIL import Image
import requests
import secrets
import config
import shutil
import os

supported_videos = ["video/mp4"]
supported_images = ["image/jpeg", "image/png"]
supported_video_types = ["anime"]
image_max_size = 10 * 1024 * 1024

# Lasciate ogni speranza, voi ch'entrate

class ChunkHelper(object):
    def __init__(self, account, uuid, upload_type):
        self.tmp_dir = f"/tmp/hikka/{account.username}/{upload_type}/"


class UploadHelper(object):
    def __init__(self, account, upload, upload_type, file_type):
        self.type = upload_type

        if self.type == "file":
            self.file_type = upload.filename.split(".")[-1]
            self.upload = upload

        if self.type == "link":
            self.file_type = upload.split(".")[-1]

            try:
                response = requests.get(upload, stream=True)
                response.raise_for_status()
                content = bytes()

            except Exception:
                response = abort("general", "file-link-down")
                flask_abort(response)

            mimetype = response.headers["Content-Type"]
            size = 0

            for block in response.iter_content(1024):
                content += block
                size += 1024

                if size > image_max_size:
                    response = abort("file", "too-big")
                    flask_abort(response)

            file = BytesIO(content)
            self.upload = FileStorage(file, content_type=mimetype)

        self.storage_name = config.storage["name"]
        self.branch = config.storage["branch"]
        self.name = secrets.token_hex(16)
        self.file_type = file_type
        self.account = account

        self.file = FileService.create(self.name, self.account)
        self.folder = utils.blake2b(self.file.created.strftime("%Y/%m"), 16, config.secret).hex()
        self.fs = storage.init_fs()

        self.storage_dir = f"{self.storage_name}/{self.branch}/{self.file_type}/{self.folder}/"
        self.tmp_dir = f"/tmp/{self.storage_name}/{self.file.name}/"

    def upload_image(self):
        if not self.is_image():
            response = abort("file", "bad-mime-type")
            flask_abort(response)

        if self.size() > image_max_size:
            response = abort("file", "too-big")
            flask_abort(response)

        storage_file_name = self.file.name + "." + "jpg"
        os.makedirs(self.tmp_dir)

        self.upload.save(self.tmp_dir + self.file.name + "." + self.file_type)
        pil = Image.open(self.tmp_dir + self.file.name + "." + self.file_type)
        width, height = pil.size

        if self.file_type == "avatar":
            avatar_size = 250

            if width != height:
                self.clean()
                response = abort("image", "not-square")
                flask_abort(response)

            if width < avatar_size:
                self.clean()
                response = abort("image", "small-image")
                flask_abort(response)

            pil = pil.resize((avatar_size, avatar_size), Image.LANCZOS)

        if self.file_type == "poster":
            max_width = 500
            if width > max_width:
                new_width = max_width
                new_height = int(new_width * height / width)
                pil = pil.resize((new_width, new_height), Image.LANCZOS)

        if self.file_type == "thumbnail":
            max_width = 250
            if width > max_width:
                new_width = max_width
                new_height = int(new_width * height / width)
                pil = pil.resize((new_width, new_height), Image.LANCZOS)

        storage_path = self.storage_dir + storage_file_name
        tmp_path = self.tmp_dir + storage_file_name
        pil.save(tmp_path, optimize=True, quality=95)

        self.finish(tmp_path, storage_path, storage_file_name)

        return self.file

    def upload_video(self):
        if not self.is_video():
            response = abort("file", "bad-mime-type")
            flask_abort(response)

        storage_file_name = self.file.name + "." + "mp4"

        os.makedirs(self.tmp_dir)
        self.upload.save(self.tmp_dir + self.file.name + "." + self.file_type)

        storage_path = self.storage_dir + storage_file_name
        tmp_path = self.tmp_dir + storage_file_name

        self.finish(tmp_path, storage_path, storage_file_name)

        return self.file

    def finish(self, tmp_path, storage_path, storage_file_name):
        self.fs.put(tmp_path, storage_path)
        self.fs.chmod(storage_path, "public-read")

        self.clean()

        self.file.path = f"/{self.branch}/{self.file_type}/{self.folder}/{storage_file_name}"
        self.file.uploaded = True
        self.file.save()

    def clean(self):
        shutil.rmtree(self.tmp_dir)

    def is_image(self):
        return self.upload.mimetype in supported_images

    def is_video(self):
        return self.upload.mimetype in supported_videos

    def size(self):
        file_size = 0
        self.upload.seek(0, os.SEEK_END)
        file_size = self.upload.tell()
        self.upload.seek(0, 0)

        return file_size
