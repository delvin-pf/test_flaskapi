from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
import bcrypt
import pytz

from src.forms import WebhookForm, LoginForm, SignupForm
from .users import User
from .users.UsersController import ALLOW_TOKEN
from .webhooks import WebHooksController


def convert_to_local_timezone(data: User):
	local_tz = pytz.timezone('America/Sao_Paulo')
	data['createdAt'] = data['createdAt'].replace(tzinfo=pytz.utc).astimezone(local_tz)
	data['updatedAt'] = data['updatedAt'].replace(tzinfo=pytz.utc).astimezone(local_tz)
	return data
	

class PagesController:
	
	@staticmethod
	def home():
		form = WebhookForm()
		
		if form.reset.data:
			form.email.data = None
			webhooks = WebHooksController.store(as_list=True)
		
		elif form.validate_on_submit() and 'submit' in request.form:
			webhooks = WebHooksController.store(form.email.data, True)
		else:
			webhooks = WebHooksController.store(as_list=True)
			
		webhooks = [convert_to_local_timezone(web) for web in webhooks]
		
		return render_template('home.html', webhooks=webhooks, form=form)
	
	
	@staticmethod
	def login():
		form = LoginForm()
		if form.validate_on_submit() and 'submit' in request.form:
			user = User.get_or_none(User.email == form.email.data)
			if not user:
				flash('Falha no login. Usuario invalido')
				return render_template('login.html', form=form)
			
			if not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
				flash('Falha no login. Senha invalida')
				return render_template('login.html', form=form)
			
			login_user(user)
			return redirect(url_for('home'))
		
		return render_template('login.html', form=form)


	@staticmethod
	def signup():
		form = SignupForm()
		
		if form.validate_on_submit() and 'submit' in request.form:
			
			if form.token.data != ALLOW_TOKEN:
				flash('Token invalido')
				return render_template('cadastro.html', form=form)
			
			user = User.get_or_none(User.email == form.email.data)
			if user:
				flash('Usuario ja existe!')
				return render_template('cadastro.html', form=form)
			
			user = User.create(
				name=form.username.data,
				email=form.email.data,
				password=bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
			)
			login_user(user)
			return redirect(url_for('home'))
			
		return render_template('cadastro.html', form=form)
		

	@staticmethod
	def logout():
		logout_user()
		flash('Logout com sucesso!')
		return redirect(url_for('login'))