from hikka.services.permissions import PermissionService
from hikka.services.files import FileService
from flask import abort as flask_abort
from hikka.tools import storage
from hikka.errors import abort
from hikka import utils
from PIL import Image
import secrets
import config
import shutil
import magic
import os

supported_videos = ["video/mp4"]
supported_images = ["image/jpeg", "image/png"]
supported_video_types = ["anime"]
max_size = 10 * 1024 * 1024

class ChunkHelper(object):
    def __init__(self, account, folder, file, upload_type, uuid):
        self.chunk_size = self.get_size(file)
        self.account = account
        self.file = file
        self.uuid = uuid

        self.tmp_dir = f"/tmp/hikka/{folder}/{upload_type}/"
        self.uuid_dir = os.path.join(self.tmp_dir, uuid)
        self.blob_file = os.path.join(self.uuid_dir, "blob")

    def load(self, size, index, total, offset):
        if size != self.chunk_size:
            self.clean()
            return abort("file", "invalid-size")

        if index >= total or index < 0:
            self.clean()
            return abort("file", "invalid-index")

        if not PermissionService.check(self.account, "global", "publishing"):
            if self.chunk_size > max_size:
                return abort("file", "too-big")

            if os.path.isfile(self.blob_file):
                if os.path.getsize(self.blob_file) > max_size:
                    return abort("file", "too-big")

        if not os.path.isdir(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        tmp_ls = os.listdir(self.tmp_dir)

        if self.uuid not in tmp_ls:
            self.clean()
            os.makedirs(self.tmp_dir)
            os.mkdir(self.uuid_dir)

        with open(self.blob_file, "ab") as blob:
            blob.seek(offset)
            blob.write(self.file.stream.read())

    def clean(self):
        shutil.rmtree(self.tmp_dir)

    def get_size(self, file):
        file_size = 0
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0, 0)

        return file_size

class UploadHelper(object):
    def __init__(self, account, path, file_type):
        self.path = path

        self.storage_name = config.storage["name"]
        self.branch = config.storage["branch"]
        self.name = secrets.token_hex(16)
        self.file_type = file_type
        self.account = account

        self.file = FileService.create(self.name, self.account)
        self.folder = utils.blake2b(self.file.created.strftime("%Y/%m"), 16, config.secret).hex()
        self.fs = storage.init_fs()

        self.storage_dir = f"{self.storage_name}/{self.branch}/{self.file_type}/{self.folder}/"
        self.mimetype = magic.from_file(path, mime=True)

    def upload_image(self):
        if not self.is_image():
            response = abort("file", "bad-mime-type")
            flask_abort(response)

        storage_file_name = self.file.name + ".jpg"

        pil = Image.open(self.path)
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

        storage_path = self.storage_dir + storage_file_name
        tmp_path = self.path + ".jpg"
        pil.save(tmp_path, optimize=True, quality=95)

        self.finish(tmp_path, storage_path, storage_file_name)

        return self.file

#     def upload_video(self):
#         if not self.is_video():
#             response = abort("file", "bad-mime-type")
#             flask_abort(response)

#         storage_file_name = self.file.name + "." + "mp4"

#         os.makedirs(self.tmp_dir)
#         self.upload.save(self.tmp_dir + self.file.name + "." + self.file_type)

#         storage_path = self.storage_dir + storage_file_name
#         tmp_path = self.tmp_dir + storage_file_name

#         self.finish(tmp_path, storage_path, storage_file_name)

#         return self.file

    def finish(self, tmp_path, storage_path, storage_file_name):
        self.fs.put(tmp_path, storage_path)
        self.fs.chmod(storage_path, "public-read")

        self.file.path = f"/{self.branch}/{self.file_type}/{self.folder}/{storage_file_name}"
        self.file.uploaded = True
        self.file.save()

    def is_image(self):
        return self.mimetype in supported_images

    def is_video(self):
        return self.mimetype in supported_videos
