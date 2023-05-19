import json

from flask import Response

from .WebhookModel import Webhook
from .WebHookSchema import WebHookSchema
from src.utils import DateTimeEncoder


class WebHooksController:
	
	@staticmethod
	def store(email: str = None, as_list: bool = False):
		"""Return list of webhooks.
		
		Args:
			email: str (optional) email for filter data.
			as_list: bool (optional) if True return data as list else return as Flask Response
		
		Returns:
			Webhhoks data
		"""
		condition = (Webhook.email == email) if email else None
		data = list(Webhook.select().where(condition).dicts())
		if as_list:
			return data
		return Response(json.dumps(data, cls=DateTimeEncoder), status=200, mimetype='application/json')
		
		
	@classmethod
	def create(cls, form: WebHookSchema):
		"""Receive webhook data and create a new log in database.
		
		Args:
			form: Webhook data.
			
		Returns:
			Response 204 - No Content
		"""
		
		action = None
		log = None
		if form.status == 'aprovado':
			log = f'Liberar o acesso do email: {form.email}'
			action = 'Acesso liberado'
		elif form.status == 'recusado':
			log = f'Informar pagamento recusado para o email {form.email}'
			action = 'Informe de recusa'
		elif form.status == 'reembolsado':
			log = f'Revogar o accesso à plataforma de {form.email}'
			action = 'Acesso revogado'
		
		Webhook.create(
			name=form.nome,
			email=form.email,
			status=form.status,
			value=form.valor,
			payment_way=form.forma_pagamento,
			installments=form.parcelas,
			action=action
		)
	
		print(action)
		
		return Response({}, status=204, mimetype='application/json')
	
