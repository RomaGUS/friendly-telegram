import hashlib
import os

def sha256(password: str):
	encoded_password = str.encode(password)
	return hashlib.sha256(encoded_password).digest()

def pebble():
	'''Generate random 32 characters string'''
	return os.urandom(16).hex()

def check_fields(fields: list, data: dict):
	'''Check if given dict `data` contain given list of keys from list `fields`.'''
	for field in fields:
		if field not in data:
			return '{} is not set'.format(field.title())

	return None

errors = {
	'account-email-exist': 'Account with this email already exists',
	'account-username-exist': 'Account with this username already exists',
	'account-activated': 'Account already activated',
	'login-failed': 'Login failed',
	'account-not-found': 'User not found',
	'user-activated': 'User already activated',
	'account-not-admin': 'User must be admin',
	'token-invalid-type': 'Invalid token type',
	'pagination-error': 'Pagination is out of range'
}
