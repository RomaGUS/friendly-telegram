from core.errors import Errors
import os

def pebble():
	"""Generate random 32 characters string"""
	return os.urandom(16).hex()

def check_fields(fields: list, data: dict):
	'''Check if given dict `data` contain given list of keys from list `fields`.'''
	for field in fields:
		if field not in data:
			return Errors.get('missing-field', '{} is not set'.format(field.title()))

	return None
