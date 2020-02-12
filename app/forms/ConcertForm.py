from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, Length, Optional


class ConcertForm(FlaskForm):
    name = StringField(label='Nazwa',
                       validators=[
                           DataRequired(message='Wprowadź nazwę.'),
                           Length(min=3, max=90, message='Nazwa powinna mieć od 3 do 90 znaków.')
                       ])
    date = DateField(label='Data',
                     format="%d.%m.%Y",
                     default=datetime.today,
                     validators=[
                         DataRequired(message='Brak daty lub wprowadzona data nie jest poprawna.'),
                     ])
    time = TimeField(label='Godzina',
                     format="%H:%M",
                     default=datetime.today,
                     validators=[
                         Optional()
                     ])
    place = StringField(label='Miejsce',
                        validators=[
                            DataRequired(message='Musisz dodać miejsce.'),
                            Length(min=3, max=90, message='Miejsce powinno mieć od 3 do 90 znaków.')
                        ])
    submit = SubmitField(label='Zapisz')
