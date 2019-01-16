from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    login = StringField(label='Login',
                        validators=[
                            DataRequired(message='Podaj login.')
                        ])
    password = PasswordField(label='Hasło',
                             validators=[
                                 DataRequired(message='Podaj hasło.')
                             ])
    remember = BooleanField(label='Zapamiętaj mnie')
    submit = SubmitField(label='Zaloguj')
