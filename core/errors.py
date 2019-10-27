class Errors():
	@classmethod
	def get(cls, name, message=''):
		if name in errors:
			error = errors[name]
			if len(message) > 0:
				error['message'] = message

			return error
		else:
			return None

errors = {
	'missing-field': {
		'code': 1,
		'message': ''
	},
	'account-email-exist': {
		'code': 2,
		'message': 'Account with this email already exists'
	},
	'account-username-exist': {
		'code': 3,
		'message': 'Account with this username already exists'
	},
	'login-failed': {
		'code': 4,
		'message': 'Login failed'
	},
	'account-not-found': {
		'code': 5,
		'message': 'User not found'
	},
	'user-activated': {
		'code': 6,
		'message': 'User already activated'
	},
	'account-not-admin': {
		'code': 9,
		'message': 'User must be admin'
	},
	'token-invalid-type': {
		'code': 10,
		'message': 'Invalid token type'
	},
	'pagination-error': {
		'code': 11,
		'message': 'Pagination is out of range'
	}
}
