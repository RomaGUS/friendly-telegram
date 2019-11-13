from hikka.services.permissions import PermissionsService
from hikka.services.users import UserService
from flask_restful import Resource
from datetime import datetime
from hikka.auth import Token
from flask import request
from hikka import utils
from hikka import api
import config
import os

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
		error = utils.check_fields(['username', 'password'], body)
		result = {'error': error, 'data': {}}

		if not result['error']:
			result['error'] = utils.errors['account-username-exist']
			account = UserService.get_by_username(body['username'])

			if account is None:
				result['error'] = utils.errors['account-email-exist']
				account_email = UserService.get_by_email(body['email'])

				if account_email is None:
					account = UserService.signup(body['username'], body['email'], body['password'])

					result['error'] = None
					result['data'] = {
						'username': account.username
					}

					if config.debug:
						# Display activation code in debug mode
						result['data']['code'] = Token.create('activation', account.username)

		return result

class Login(Resource):
	def post(self):
		body = request.get_json()
		error = utils.check_fields(['email', 'password'], body)
		result = {'error': error, 'data': {}}

		if not result['error']:
			result['error'] = utils.errors['account-not-found']
			account = UserService.get_by_email(body['email'])

			if account is not None:
				result['error'] = utils.errors['login-failed']
				login = UserService.login(body['password'], account.password)

				if login:
					UserService.update(account, login=datetime.now)
					token = Token.create('login', account.username)
					data = Token.validate(token)

					result['error'] = None
					result['data'] = {
						'token': token,
						'expire': data['payload']['expire'],
						'username': data['payload']['username']
					}

		return result

class Activate(Resource):
	def get(self, token):
		data = Token.validate(token)
		result = {'error': utils.errors['token-invalid-type'], 'data': {}}

		if data['valid']:
			result['error'] = utils.errors['account-not-found']
			account = UserService.get_by_username(data['payload']['username'])

			if account is not None:
				result['error'] = utils.errors['account-activated']
				activated = PermissionsService.check(account, 'accounts', 'activated')

				if not activated and data['payload']['action'] == 'activation':
					PermissionsService.add(account, 'accounts', 'activated')

					result['error'] = None
					result['data'] = {
						'username': account.username,
						'activated': True
					}

		return result

api.add_resource(Upload, '/api/upload')
api.add_resource(Join, '/api/join')
api.add_resource(Login, '/api/login')
api.add_resource(Activate, '/api/activate/<string:token>')
