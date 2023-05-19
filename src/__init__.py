from flask import Flask, g
from flask_login import login_required
from flask_login import LoginManager

from database import database
# Routes
from modules.webhooks.webhooks_router import webhooks_router
from modules.users.users_router import users_router
from modules.users.UsersController import UserController
from modules.Pages import PagesController

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flasapihashtag'
app.config['DEBUG'] = True
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def get_user(user_id):
	return UserController.load_user_by_id(user_id)


@app.before_request
def before_request():
	if 'db' not in g:
		g.db = database
	if g.db.is_closed():
		g.db.connect()


@app.after_request
def after_request(response):
	g.db.close()
	return response


@app.route('/')
def index():
	return {'g': 'hola'}


@app.route('/login', methods=['GET', 'POST'])
def login():
	return PagesController.login()


@app.route('/cadastro', methods=['GET', 'POST'])
def signup():
	return PagesController.signup()


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	return PagesController.home()


@app.route('/sair', methods=['GET'])
@login_required
def logout():
	return PagesController.logout()


app.register_blueprint(webhooks_router)
app.register_blueprint(users_router)
