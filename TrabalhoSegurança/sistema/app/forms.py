from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Usuario

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembre Me')

class RegistraUsuarioForm(FlaskForm):
    name = StringField('Nome:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    username = StringField('Usuário:', validators=[DataRequired()])
    password = PasswordField('Senha:', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirmação de Senha:', validators=[DataRequired(), EqualTo('password')])
  

    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Usuário já existente!')
 
class MessageForm(FlaskForm):    # Create Message Form
    body = StringField('D:', validators=[DataRequired()])
