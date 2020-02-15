from hikka.services.models.permission import Permission
from hikka.services.models.user import User

class PermissionService:
    @classmethod
    def get(cls, scope: str, name: str) -> Permission:
        permission = Permission.objects().filter(scope=scope, name=name).first()
        if permission is None:
            permission = Permission(name=name, scope=scope)
            permission.save()

        return permission

    @classmethod
    def add(cls, user: User, scope: str, name: str):
        permission = cls.get(scope=scope, name=name)
        if permission not in user.permissions:
            user.permissions.append(permission)

        user.save()

    @classmethod
    def remove(cls, user: User, scope: str, name: str):
        permission = cls.get(scope=scope, name=name)
        if permission in user.permissions:
            index = user.permissions.index(permission)
            user.permissions.pop(index)

        user.save()

    @classmethod
    def check(cls, user: User, scope: str, name: str) -> bool:
        permission = cls.get(scope=scope, name=name)
        if permission in user.permissions:
            return True

        admin = cls.get("global", "admin")
        if admin in user.permissions:
            return True

        return False
