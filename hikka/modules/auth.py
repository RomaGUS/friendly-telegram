from hikka.services.permissions import PermissionsService
from hikka.services.users import UserService
from flask_restful import Resource
from datetime import datetime
from hikka.auth import Token
from flask import request
from hikka import utils
from hikka import api
import config

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

api.add_resource(Join, '/api/join')
api.add_resource(Login, '/api/login')
api.add_resource(Activate, '/api/activate/<string:token>')
