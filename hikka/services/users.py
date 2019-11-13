from hikka.services.func import update_document
from hikka.services.models.user import User
import hikka.auth as auth
from typing import List

class UserService:
	@classmethod
	def signup(cls, username: str, email: str, password: str) -> User:
		user = User(email=email, username=username, password=auth.hashpwd(password))
		user.save()
		return user

	@classmethod
	def login(cls, password: str, bcrypt_hash: str) -> bool:
		return auth.checkpwd(password, bcrypt_hash)

	@classmethod
	def update(cls, user: User, **kwargs):
		user = update_document(user, kwargs)
		user.save()

	@classmethod
	def get_by_id(cls, uid: str):
		user = User.objects().filter(id=uid).first()
		return user

	@classmethod
	def get_by_email(cls, email: str):
		user = User.objects().filter(email=email).first()
		return user

	@classmethod
	def get_by_username(cls, username: str):
		user = User.objects().filter(username=username).first()
		return user

	@classmethod
	def list(cls, page=1, limit=10) -> List[User]:
		offset = page * limit
		accounts = User.objects().filter().limit(limit).skip(offset)
		return list(accounts)
