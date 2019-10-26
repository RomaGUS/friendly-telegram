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
	'event-create-failed': {
		'code': 7,
		'message': 'Event creation failed'
	},
	'ticker-not-found': {
		'code': 8,
		'message': 'Ticker not found'
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
	},
	'event-not-found': {
		'code': 13,
		'message': 'Event not found'
	},
	'ticker-exist': {
		'code': 14,
		'message': 'Coin with this ticker already exists'
	},
	'account-already-clicked': {
		'code': 15,
		'message': 'User already clicked'
	},
	'event-is-finished': {
		'code': 16,
		'message': 'Event is finished'
	}
}
