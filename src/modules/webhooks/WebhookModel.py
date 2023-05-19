from datetime import datetime

from peewee import Model, AutoField, CharField, DateTimeField, IntegerField, FloatField

from src.database import database


class Webhook(Model):
	id = AutoField(primary_key=True)
	name = CharField()
	email = CharField()
	status = CharField()
	value = FloatField()
	payment_way = CharField()
	installments = IntegerField()
	action = CharField()
	createdAt = DateTimeField(default=datetime.now)
	updatedAt = DateTimeField(default=datetime.now)
	
	class Meta:
		database = database
		table_name = 'webhooks'
