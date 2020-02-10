from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField, FieldList, FormField, SelectField, BooleanField
from wtforms.validators import Optional, Regexp, DataRequired


class SliderEntry(FlaskForm):
    slide_type = SelectField(label='Typ',
                             choices=[
                                 ('v', 'Filmik z youtube'),
                                 ('i', 'Obraz')
                             ],
                             validators=[
                                 DataRequired(message='Musisz podać typ.'),
                             ])
    youtube = StringField(label='Filmik',
                          validators=[
                              Optional(),
                              Regexp(
                                  regex='^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/('
                                        '?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(\?\S*)?$',
                                  # https://stackoverflow.com/questions/3717115/regular-expression-for-youtube-links
                                  message='Podany link nie jest poprawny.'
                              )
                          ])
    picture = FileField(label='Zdjęcie',
                        validators=[
                            Optional(),
                            FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                        ])
    display = BooleanField(label='Wyświetl slajd')


class SliderForm(FlaskForm):
    slides = FieldList(FormField(SliderEntry), min_entries=8, max_entries=8)
    submit = SubmitField(label='Zapisz')
