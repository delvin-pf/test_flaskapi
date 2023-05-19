import os
from contextvars import ContextVar
from dotenv import load_dotenv
from peewee import _ConnectionState, MySQLDatabase

load_dotenv()

ENV = os.environ.get('ENV')
prefix = '' if ENV in ['production', 'development'] else 'REMOTE_PRD_'

DATABASE_NAME = os.environ.get(f'{prefix}DATABASE_NAME')
DATABASE_HOST = os.environ.get(f'{prefix}DATABASE_HOST')
DATABASE_PORT = int(os.environ.get(f'{prefix}DATABASE_PORT'))
DATABASE_USER = os.environ.get(f'{prefix}DATABASE_USER')
DATABASE_PASS = os.environ.get(f'{prefix}DATABASE_PASSWORD')

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

try:
	database.connect()
	print('\033[92m{}\033[0m'.format('Database conection successful!'))
except Exception as e:
	raise Exception('\033[91m{}\033[0m'.format('Database conection failed!'))
finally:
	if not database.is_closed():
		database.close()


