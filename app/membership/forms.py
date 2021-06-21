from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import TextField, PasswordField, FileField
from wtforms import validators
from wtforms.validators import InputRequired, Email, DataRequired

# payment forms
class PaymentForm(FlaskForm):
    photo = FileField('Upload ID photo', id='photo')
    name = TextField('Cardholder Name', id="cardholder", validators=[DataRequired()])
    cvv = PasswordField('CVV', id="cvv", validators=[DataRequired()])
    expiry = TextField('Expiry Date', id="expiry", validators=[DataRequired()])