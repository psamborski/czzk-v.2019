from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo


class SettingsForm(FlaskForm):
    login = StringField(label='Login',
                        validators=[
                            DataRequired(message='Podaj login.')
                        ])
    email = EmailField(label='Adres e-mail',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Email(message='Niepoprawny adres e-mail.')
                       ])
    submit = SubmitField('Zapisz')


class PasswordForm(FlaskForm):
    password = PasswordField(label='Nowe hasło:',
                             validators=[
                                 DataRequired()
                             ])
    confirm_password = PasswordField(label='Powtórz hasło:',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ])
    submit = SubmitField(label='Zapisz')
