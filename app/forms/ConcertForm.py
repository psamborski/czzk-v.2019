from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ConcertForm(FlaskForm):
    title = StringField(label='Nazwa:',
                        validators=[
                            DataRequired(message='Wprowadź nazwę.'),
                            Length(min=3, max=70, message='Nazwa powinna mieć od 3 do 120 znaków.')
                        ])
    date = DateField(label='Data:',
                     format="%d.%m.%Y",
                     default=datetime.today,
                     validators=[
                         DataRequired(message='Brak daty lub wprowadzona data nie jest poprawna.'),
                     ])
    place = StringField(label='Miejsce:',
                        validators=[
                            DataRequired(message='Musisz dodać miejsce.'),
                            Length(min=3, max=70, message='Miejsce powinno mieć od 3 do 120 znaków.')
                        ])
    submit = SubmitField(label='Zapisz')
