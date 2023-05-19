from src.database import database
from src.modules.users import User
from src.modules.webhooks import Webhook


def create_tables():
	with database.atomic():
		try:
			database.create_tables([Webhook, User])
			print('Tables created')
		except Exception as e:
			print('Error: ', e)


def drop_tables():
	with database.atomic():
		try:
			database.drop_tables([Webhook, User])
			print('Tables dropped')
		except Exception as e:
			print('ERROR:', e)
			

if __name__ == '__main__':
	create_tables()
	# drop_tables()
	
