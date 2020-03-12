from hikka.services.files import FileService
from hikka.errors import abort
from hikka.tools import spaces
from hikka import utils
from PIL import Image
import secrets
import config
import shutil
import os

supported_videos = ["video/mp4"]
supported_images = ["image/jpeg", "image/png"]
supported_video_types = ["anime"]
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
        if not self.is_image():
            return abort("file", "bad-mime-type")

        if self.size() > image_max_size:
            return abort("file", "too-big")

        spaces_file_name = self.file.name + "." + "jpg"
        os.makedirs(self.tmp_dir)

        self.upload.save(self.tmp_dir + self.file.name + "." + self.file_type)
        pil = Image.open(self.tmp_dir + self.file.name + "." + self.file_type)
        width, height = pil.size

        if self.upload_type == "avatar":
            avatar_size = 250

            if width != height:
                self.clean()
                return abort("image", "not-square")

            if width < avatar_size:
                self.clean()
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

        self.clean()

        self.file.path = f"/{self.upload_type}/{self.folder}/{spaces_file_name}"
        self.file.uploaded = True
        self.file.save()

        return self.file

    def upload_video(self):
        if not self.is_video():
            return abort("file", "bad-mime-type")

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
