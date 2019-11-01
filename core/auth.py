from datetime import datetime, timedelta
from core import utils
import bcrypt
import config
import base58
import hmac
import json

def hashpwd(password: str) -> str:
	return bcrypt.hashpw(utils.sha256(password), bcrypt.gensalt()).decode()

def checkpwd(password, bcrypt_hash) -> bool:
	return bcrypt.checkpw(utils.sha256(password), str.encode(bcrypt_hash))

# https://gist.github.com/darelf/190bc97b29e91509534d7535ebde4762
class JWT():
	@classmethod
	def create_signed_token(cls, key, data):
		"""
		Create a complete JWT token. Exclusively uses sha256
		HMAC.
		"""
		header = json.dumps({'typ': 'JWT', 'alg': 'HS256'}).encode('utf-8')
		henc = base58.b58encode_check(header).decode()

		payload = json.dumps(data).encode('utf-8')
		penc = base58.b58encode_check(payload).decode()

		hdata = henc + '.' + penc

		d = hmac.new(key, hdata.encode('utf-8'), 'sha256')
		dig = d.digest()
		denc = base58.b58encode_check(dig).decode()

		token = hdata + '.' + denc
		return token

	@classmethod
	def verify_signed_token(cls, key, token):
		"""
		Decodes the payload in the token and returns a tuple
		whose first value is a boolean indicating whether the
		signature on this token was valid, followed by the
		decoded payload.
		"""
		try:
			(header, payload, sig) = token.split('.')
			hdata = header + '.' + payload

			d = hmac.new(key, hdata.encode('utf-8'), 'sha256')
			dig = d.digest()
			denc = base58.b58encode_check(dig).decode()

			verified = hmac.compare_digest(sig, denc)
			payload_data = json.loads(base58.b58decode_check(payload).decode())
			return {
				'valid': verified,
				'payload': payload_data
			}
		except Exception:
			return {
				'valid': False,
				'payload': {}
			}

class Token():
	@classmethod
	def create(cls, action, user, days=3):
		"""
		Token valid for 3 days by default
		"""
		expire = int(datetime.timestamp(datetime.now() + timedelta(days=days)))
		return JWT.create_signed_token(utils.sha256(config.secret), {
			'action': action,
			'username': user,
			'expire': expire}
		)

	@classmethod
	def validate(cls, token):
		data = JWT.verify_signed_token(utils.sha256(config.secret), token)
		if 'expire' not in data['payload']:
			data['valid'] = False
		else:
			if data['payload']['expire'] < int(datetime.timestamp(datetime.now())):
				data['valid'] = False

		return data
