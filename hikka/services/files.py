from hikka.services.models.file import File
from hikka.services.models.user import User
from hikka import spaces

class FileService:
    @classmethod
    def create(cls, name: str, account: User) -> File:
        file = File(account=account, name=name)
        file.save()
        return file

    @classmethod
    def get_by_name(cls, name: str):
        file = File.objects().filter(name=name).first()
        return file

    @classmethod
    def destroy(cls, file: File):
        if file.uploaded and file.path is not None:
            fs = spaces.init_fs()
            fs.rm(file.path())

        file.delete()
