import os
from contextvars import ContextVar
from dotenv import load_dotenv
from peewee import _ConnectionState, MySQLDatabase

load_dotenv()

DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT'))
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASS = os.environ.get('DATABASE_PASSWORD')

db_state_default = {
	"closed": None,
	"conn": None,
	"ctx": None,
	"transactions": None
}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
	def __init__(self, **kwargs):
		super().__setattr__('_state', db_state)
		super().__init__(**kwargs)
	
	
	def __setattr__(self, name, value):
		self._state.get()[name] = value
	
	
	def __getattr__(self, name):
		return self._state.get()[name]


database = MySQLDatabase(
	DATABASE_NAME,
	host=DATABASE_HOST,
	port=DATABASE_PORT,
	user=DATABASE_USER,
	password=DATABASE_PASS,
	autorollback=True
)
database._state = PeeweeConnectionState()