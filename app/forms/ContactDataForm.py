from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Email, Regexp


class ContactDataForm(FlaskForm):
    email = EmailField(label='Adres e-mail',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Email(message='Niepoprawny adres e-mail.')
                       ])
    phone = TelField(label='Numer telefonu',
                     validators=[
                         DataRequired(message='To pole nie może być puste.'),
                         Regexp(r'(?<!\w)(\(?(\+)?\d{2}\)?)?[ -]?\d{3}[ -]?((\d{3}[ -]?\d{3})|(\d{2}[ -]?\d{2}))(?!\w)',
                                message='To pole nie zawiera poprawnego numeru telefonu.')
                     ])
