from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, TextAreaField
from wtforms.validators import DataRequired, Length


class TextEntry(FlaskForm):  # for omitting csrf problem
    title = StringField(label='Tytuł',
                        validators=[
                            DataRequired(message='Podaj tytuł.'),
                            Length(min=3, max=120, message='Podany tekst powinien mieć od 3 do 120 znaków.')
                        ])
    content = TextAreaField(label='Treść',
                            validators=[
                                DataRequired(message='To pole nie może być puste.'),
                                Length(min=5, max=1024,
                                       message='Wprowadzony tekst powinien mieć od 5 do 1024 znaków.')],
                            )


class AboutTextForm(FlaskForm):
    chapters = FieldList(FormField(TextEntry), min_entries=3, max_entries=3)
    submit = SubmitField(label='Zapisz')


class MusicTextForm(FlaskForm):
    chapters = FieldList(FormField(TextEntry), min_entries=2, max_entries=2)
    submit = SubmitField(label='Zapisz')
