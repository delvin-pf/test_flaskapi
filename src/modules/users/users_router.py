from flask import Blueprint, request, Response
from pydantic import ValidationError

from .UsersController import UserController
from .UserSchema import UserSchema, UserLoginSchema


users_router = Blueprint('users', __name__, url_prefix='/api/users')


@users_router.route('', methods=['POST'])
def create():
	try:
		form = UserSchema(**request.form)
		return UserController.create(form)
	
	except ValidationError as e:
		response = e.json()
		return Response(status=400, response=response, mimetype='application/json')
	
	
@users_router.route('/login', methods=['POST'])
def login():
	form = request.form
	try:
		user = UserLoginSchema(**form)
		return UserController.login(user)

	except ValidationError as e:
		response = e.json()
		return Response(status=400, response=response, mimetype='application/json')
