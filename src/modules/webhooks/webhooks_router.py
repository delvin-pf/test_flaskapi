import json
import re

from flask import Blueprint, request, Response
from pydantic import ValidationError

from .WebhooksController import WebHooksController
from .WebHookSchema import WebHookSchema
from src.utils import jwt_required


webhooks_router = Blueprint('webhooks', __name__, url_prefix='/api/webhooks')


@webhooks_router.route('', methods=['GET'])
@jwt_required
def store():
	email = request.args.get('email')
	if email:
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		if not re.fullmatch(regex, email):
			return Response(
				status=400,
				response=json.dumps({'message': 'email must be a valid email address'}),
				mimetype='application/json'
			)
	return WebHooksController.store(email)


@webhooks_router.route('', methods=['POST'])
def create():
	data = request.get_data().decode('utf-8')
	data_dict = json.loads(data)
	
	try:
		webhook = WebHookSchema(**data_dict)
		return WebHooksController.create(webhook)
	except ValidationError as e:
		response = e.json()
		return Response(status=400, response=response, mimetype='application/json')
