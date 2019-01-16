from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class AlbumForm(FlaskForm):
    title = StringField(label='Tytuł:',
                        validators=[
                            DataRequired(message='Musisz podać tytuł.'),
                            Length(min=3, max=120, message='Podany tytuł powinien mieć od 3 do 120 znaków.')
                        ])
    year = StringField(label='Rok wydania:',
                       validators=[
                           DataRequired(message='Musisz podać rok wydania.'),
                           Regexp(regex='^(19|20)\d{2}$', message='Niepoprawny rok.')
                       ])
    description = StringField(label='Opis:',
                              validators=[
                                  DataRequired(message='Musisz dodać opis.'),
                                  Length(min=3, max=1024, message='Podany opis musi mieć od 3 do 1024 znaków.')
                              ])
    cover = FileField(label='Miniaturka:',
                      validators=[
                          DataRequired(message='Musisz dodać okładkę (lub inne zdjęcie).'),
                          FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                      ])
    submit = SubmitField(label='Zapisz')
