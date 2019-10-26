from datetime import datetime, timedelta
from core import jwt
import hashlib
import bcrypt
import config

def sha256(password: str):
	encoded_password = str.encode(password)
	return hashlib.sha256(encoded_password).digest()

def hashpwd(password: str) -> str:
	return bcrypt.hashpw(sha256(password), bcrypt.gensalt()).decode()

def checkpwd(password, bcrypt_hash) -> bool:
	return bcrypt.checkpw(sha256(password), str.encode(bcrypt_hash))

class Token():
	@classmethod
	def create(cls, action, user, days=3):
		# Token valid for 3 days by default
		expire = int(datetime.timestamp(datetime.now() + timedelta(days=days)))
		return jwt.create_signed_token(sha256(config.secret), {
			'action': action,
			'username': user,
			'expire': expire}
		)

	@classmethod
	def validate(cls, token):
		data = jwt.verify_signed_token(sha256(config.secret), token)
		if 'expire' not in data['payload']:
			data['valid'] = False
		else:
			if data['payload']['expire'] < int(datetime.timestamp(datetime.now())):
				data['valid'] = False

		return data
