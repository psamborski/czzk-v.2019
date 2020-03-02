from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class SizeTableForm(FlaskForm):
    content = TextAreaField(label='Tabela',
                            validators=[
                                DataRequired(message='To pole nie może być puste.'),
                                Length(max=8192,
                                       message='Wprowadzony tekst powinien mieć do 8192 znaków.')],
                            )
    submit = SubmitField(label='Zapisz')
