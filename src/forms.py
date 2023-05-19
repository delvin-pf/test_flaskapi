from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, StopValidation


def email_if_empty(form, field):
	if field.data == '':
		raise StopValidation()
		

class SignupForm(FlaskForm):
	username = StringField('Usuario', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = StringField('Password', validators=[DataRequired(), Length(6, 20)])
	token = StringField('Token')
	submit = SubmitField('Criar conta')
	

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = StringField('Password', validators=[DataRequired(), Length(6, 20)])
	submit = SubmitField('Login')
	
	
class WebhookForm(FlaskForm):
	email = StringField('Email', validators=[email_if_empty, Email()])
	submit = SubmitField('Pesquisar')
	reset = SubmitField('Resetar a busca')
	
	
	
			
		
