from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField, FieldList, FormField
from wtforms.validators import Optional, Regexp


class SliderEntry(FlaskForm):
    youtube = StringField(label='Filmik',
                          validators=[
                              Optional(),
                              Regexp(
                                  regex='http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&('
                                        'amp;)?‌​[\w\?‌​=]*)?',
                                  # https://stackoverflow.com/questions/3717115/regular-expression-for-youtube-links
                                  message='Podany link nie jest poprawny.'
                              )
                          ])
    picture = FileField(label='Zdjęcie',
                        validators=[
                            Optional(),
                            FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                        ])


class SliderForm(FlaskForm):
    slides = FieldList(FormField(SliderEntry), min_entries=1)
    submit = SubmitField(label='Zapisz')
