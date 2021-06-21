from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms import validators
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    email    = TextField('Email' , id='email_login' , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login' , validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username' , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email' , id='email_create' , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create' , validators=[DataRequired()])


class ForgotPasswordForm(FlaskForm):
    email = TextField('Email', id='email-id', validators=[DataRequired()])


class ResetPassswordForm(FlaskForm):
    password = PasswordField('Password', id='pwd_login' , validators=[DataRequired()])
