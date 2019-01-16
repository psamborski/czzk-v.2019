from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class GalleryForm(FlaskForm):
    rider = FileField(label='Rider:',
                      validators=[
                          DataRequired(message='Musisz dodać rider.'),
                          FileAllowed(['pdf', 'docx'], message='Nieprawidłowy format pliku (.pdf, .docx).')
                      ])
    submit = SubmitField(label='Zapisz')
