from models.permission import UserPermission
from models.user import User

class UserPermissionsService:
	@classmethod
	def get(cls, scope: str, name: str) -> UserPermission:
		permission = UserPermission.objects().filter(scope=scope, name=name).first()
		if permission is None:
			permission = UserPermission(name=name, scope=scope)
			permission.save()

		return permission

	@classmethod
	def add(cls, user: User, scope: str, name: str):
		permission = cls.get(name=name, scope=scope)
		if permission.id not in user.rights:
			user.rights.append(permission.id)
		user.save()

	@classmethod
	def remove(cls, user: User, scope: str, name: str):
		permission = cls.get(scope=scope, name=name)
		if permission.id in user.permission:
			index = user.permission.index(permission.id)
			user.permission.pop(index)
		user.save()

	@classmethod
	def check(cls, user: User, scope: str, name: str) -> bool:
		permission = UserPermission.objects().filter(scope=scope, name=name).first()
		if permission is not None and permission.id in user.rights:
			return True

		return False
