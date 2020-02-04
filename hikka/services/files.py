from hikka.services.models.file import File
from hikka.services.models.user import User

class FileService:
    @classmethod
    def create(cls, name: str, account: User) -> File:
        file = File(account=account, name=name)
        file.save()
        return file

    @classmethod
    def get_by_name(cls, name: str):
        team = File.objects().filter(name=name).first()
        return team
