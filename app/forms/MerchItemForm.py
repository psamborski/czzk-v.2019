from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class MerchItemForm(FlaskForm):
    name = StringField(label='Nazwa',
                       validators=[
                           DataRequired(message='Musisz podać tytuł.'),
                           Length(min=3, max=120, message='Podana nazwa powinna mieć od 3 do 120 znaków.')
                       ])
    short_name = StringField(label='Krótka nazwa (do wyświetlenia w spisie)',
                             validators=[
                                 DataRequired(message='Musisz podać tytuł.'),
                                 Length(min=3, max=11, message='Skrócona nazwa powinna mieć od 3 do 11 znaków.')
                             ])
    description = StringField(label='Opis',
                              validators=[
                                  DataRequired(message='Musisz dodać opis.'),
                                  Length(min=3, max=1024, message='Podany opis musi mieć od 3 do 1024 znaków.')
                              ])
    photo = FileField(label='Zdjęcie (.jpg, .png)',
                      validators=[
                          Optional(),
                          FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                      ])
    animation = FileField(label='Animacja (.gif - nieobowiązkowa)',
                          validators=[
                              Optional(),
                              FileAllowed(['gif'], message='Nieprawidłowy format pliku (.gif).')
                          ])
    submit = SubmitField(label='Zapisz')
