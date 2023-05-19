from datetime import datetime

from peewee import Model, AutoField, CharField, DateTimeField

from src.database import database


class User(Model):
	id = AutoField(primary_key=True)
	name = CharField()
	email = CharField()
	password = CharField()
	createdAt = DateTimeField(default=datetime.now)
	updatedAt = DateTimeField(default=datetime.now)
	
	class Meta:
		database = database
		table_name = 'users'
