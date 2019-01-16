from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length


class TextEntry(FlaskForm):
    title = StringField(label='Tytuł',
                        validators=[
                            DataRequired(message='Podaj tytuł.'),
                            Length(min=3, max=120, message='Podany tekst powinien mieć od 3 do 120 znaków.')
                        ])
    content = StringField(label='Treść',
                          validators=[
                              DataRequired(message='Musisz dodać treść.')
                          ])


class AboutTextForm(FlaskForm):
    chapters = FieldList(FormField(TextEntry), min_entries=3, max_entries=3)
    submit = SubmitField(label='Zapisz')


class KazikTextForm(FlaskForm):
    chapters = FieldList(FormField(TextEntry), min_entries=5, max_entries=5)
    submit = SubmitField(label='Zapisz')
