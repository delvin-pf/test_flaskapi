import json
import os

import bcrypt
import jwt
from dotenv import load_dotenv
from flask import Response

from src.modules.users.UserSchema import UserSchema, UserLoginSchema
from .UserModel import User

load_dotenv()
ALLOW_TOKEN = os.environ.get('TOKEN')
SECRET = os.environ.get('SECRET')


class UserController:
	"""Process requests to users endpoint"""
	
	@classmethod
	def login(cls, form: UserLoginSchema):
		"""Login an user and return a JWT token in Flask Response class
		
		Args:
			form: Form with login data
			
		Returns: Response
		"""
		
		user = User.get_or_none(User.email == form.email)
		if not user:
			return Response(
				json.dumps({'message': 'User no exist!'}),
				status=400,
				mimetype='application/json'
			)
		if not cls.__check_password(user.password, form.password):
			return Response(
				json.dumps({'message': 'Invalid credentials'}),
				status=401,
				mimetype='application/json'
			)
		payload = {
			'id': user.id,
			'name': user.name,
			'email': user.email
		}
		
		token = jwt.encode(payload, SECRET, algorithm="HS256")
		return {'token': f'Bearer {token}'}
	
	
	@classmethod
	def create(cls, form: UserSchema) -> Response:
		"""Create a new user and return user data with id in Response.
		
		Args:
			form: Object with user data.
			
		Returns:
			Response in json format
		"""
		if form.token != ALLOW_TOKEN:
			return Response(
				json.dumps({'message': 'Invalid token!'}),
				status=400,
				mimetype='application/json'
			)
		
		user = User.get_or_none(User.email == form.email)
		if user:
			return Response(
				json.dumps({'message': 'User already exists!'}),
				status=400,
				mimetype='application/json'
			)
		
		hashed_pass = bcrypt.hashpw(form.password.encode('utf-8'), bcrypt.gensalt())
		
		user = User.create(name=form.name, email=form.email, password=hashed_pass)
		
		return Response(
			json.dumps({
				'id': user.id,
				'name': user.name,
				'email': user.email
			}),
			status=201,
			mimetype='application/json'
		)
	
	
	@classmethod
	def __check_password(cls, plain_pass, hashed_pass):
		
		return bcrypt.checkpw(plain_pass, hashed_pass)
	
	
	@staticmethod
	def load_user_by_id(user_id: int) -> User | None:
		"""Return data user.
		
		Args:
			user_id: User ID in database.
			
		Returns:
			User model instance if users exist else None
		"""
		return User.get_or_none(User.id == user_id)
