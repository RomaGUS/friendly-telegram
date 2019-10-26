import base64
import hmac
import json

# https://gist.github.com/darelf/190bc97b29e91509534d7535ebde4762
def create_signed_token(key, data):
	"""
	Create a complete JWT token. Exclusively uses sha256
	HMAC.
	"""
	header = json.dumps({'typ': 'JWT', 'alg': 'HS256'}).encode('utf-8')
	henc = base64.urlsafe_b64encode(header).decode().strip('=')

	payload = json.dumps(data).encode('utf-8')
	penc = base64.urlsafe_b64encode(payload).decode().strip('=')

	hdata = henc + '.' + penc

	d = hmac.new(key, hdata.encode('utf-8'), 'sha256')
	dig = d.digest()
	denc = base64.urlsafe_b64encode(dig).decode().strip('=')

	token = hdata + '.' + denc
	return token


def verify_signed_token(key, token):
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
		denc = base64.urlsafe_b64encode(dig).decode().strip('=')

		verified = hmac.compare_digest(sig, denc)
		payload += '=' * (-len(payload) % 4)
		payload_data = json.loads(base64.urlsafe_b64decode(payload).decode())
		return {
			'valid': verified,
			'payload': payload_data
		}
	except Exception:
		return {
			'valid': False,
			'payload': {}
		}
