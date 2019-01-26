from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class ContactForm(FlaskForm):
    email = EmailField(label='Twój e-mail',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Email(message='Niepoprawny adres e-mail.')
                       ])
    topic = StringField(label='Temat',
                        validators=[
                            DataRequired(message='To pole nie może być puste.'),
                            Length(min=3, max=120, message='Wprowadzony tekst powinien mieć od 3 do 120 znaków.')
                        ])
    message = TextAreaField(label='Wiadomość',
                            validators=[
                                DataRequired(message='To pole nie może być puste.'),
                                Length(min=5, max=1024, message='Wprowadzony tekst powinien mieć od 5 do 1024 znaków.')
                            ])
    submit = SubmitField(label='WYŚLIJ')


class MerchContactForm(FlaskForm):
    email = EmailField(label='Twój e-mail',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Email(message='Niepoprawny adres e-mail.')
                       ])
    message = TextAreaField(label='Informacje dodatkowe (np. ilość, rozmiar):',
                            validators=[
                                DataRequired(message='To pole nie może być puste.'),
                                Length(min=5, max=1024, message='Wprowadzony tekst powinien mieć od 5 do 1024 znaków.')
                            ])
    submit = SubmitField(label='Wyślij')
