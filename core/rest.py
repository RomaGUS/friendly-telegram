from flask_restful import Resource
from services.users import UserService
from core.errors import errors
from datetime import datetime
from core.auth import Token
from flask import request
from core import utils
import config
import os

def init(api):
	api.add_resource(Upload, '/api/upload')
	api.add_resource(Join, '/api/join')
	api.add_resource(Activate, '/api/activate/<string:token>')

class Upload(Resource):
	def post(self):
		if 'upload' in request.files:
			# hls = Hls('hikka/konosuba/hls/')
			# Return True here and start processing video in separate thread
			# hls.ffmpeg()
			# hls.process()

			# ToDo: support different file types
			# Only mp4 for now
			file = request.files['upload']
			if file.mimetype in ['video/mp4']:
				name = utils.pebble()
				tmp_dir = '/tmp/hikka-{}/'.format(name)
				tmp_file = tmp_dir + '{}.mp4'.format(name)

				if not os.path.exists(tmp_dir):
					os.makedirs(tmp_dir)

				with open(tmp_file, 'wb') as file_local:
					file_local.write(file.read())

				return True

			return False
		else:
			return False

class Join(Resource):
	def post(self):
		body = request.get_json()
		result = {'error': None, 'data': {}}
		result['error'] = utils.check_fields(['username', 'password'], body)

		if not result['error']:
			account = UserService.get_by_username(body['username'])
			if account is None:
				account_email = UserService.get_by_email(body['email'])
				if account_email is None:
					account = UserService.signup(body['username'], body['email'], body['password'])
					result['data'] = {
						'username': account.username
					}

					if config.debug:
						result['data']['email'] = Token.create('activation', account.username)
				else:
					result['error'] = errors['account-email-exist']

			else:
				result['error'] = errors['account-username-exist']

		return result

class Login(Resource):
	def post(self):
		body = request.get_json()
		result = {'error': None, 'data': {}}
		result['error'] = utils.check_fields(['email', 'password'], body)

		if not result['error']:
			account = UserService.get_by_email(body['email'])
			if account is not None:
				if UserService.login(body['password'], account.password):
					UserService.update(account, login=datetime.now)
					token = Token.create('login', account.username)
					data = Token.validate(token)

					result['data'] = {
						'token': token,
						'expire': data['payload']['expire'],
						'username': data['payload']['username'],
						'role': 'admin' if account.admin else 'user'
					}

				else:
					result['error'] = errors['login-failed']

			else:
				result['error'] = errors['account-not-found']

		return result

class Activate(Resource):
	def get(self, token):
		data = Token.validate(token)
		result = {'error': None, 'data': {}}

		if data['valid']:
			account = UserService.get_by_username(data['payload']['username'])
			if account is not None:
				if not account.activated:
					if data['payload']['action'] == 'activation':
						UserService.update(account, activated=True)
						result['data'] = {
							'username': account.username,
							'activated': account.activated
						}
				else:
					result['error'] = errors['account-activated']
					
			else:
				result['error'] = errors['account-not-found']

		else:
			result['error'] = errors['token-invalid-type']

		return result
