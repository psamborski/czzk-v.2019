from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length


class GalleryForm(FlaskForm):
    title = StringField(label='Tytuł:',
                        validators=[
                            DataRequired(message='Musisz podać tytuł.'),
                            Length(min=3, max=120, message='Podany tytuł powinien mieć od 3 do 120 znaków.')
                        ])
    thumbnail = FileField(label='Miniaturka:',
                          validators=[
                              DataRequired(message='Musisz dodać miniaturkę.'),
                              FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                          ])
    images = FileField(label='Obrazy:',
                       render_kw={'multiple': True},
                       validators=[
                           DataRequired(message='Musisz dodać obrazy.'),
                           FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku(ów) (.jpg, .png).')
                       ])
    submit = SubmitField(label='Zapisz')
