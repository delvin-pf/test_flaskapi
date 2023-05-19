from functools import wraps
from flask import request, current_app
import jwt


def jwt_required(func):
	@wraps(func)
	def decorated(*args, **kwargs):
		token = request.headers.get('Authorization')
		if not token:
			return {'message': 'Authentication token missing'}, 401
		
		try:
			print(token)
			jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			return {'message': 'Expired token'}, 401
		except jwt.InvalidTokenError:
			return {'message': 'Invalid token'}, 401
		
		return func(*args, **kwargs)
	
	
	return decorated
