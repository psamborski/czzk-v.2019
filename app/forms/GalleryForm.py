from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.resources.GalleriesResource import Galleries


class GalleryForm(FlaskForm):
    def __init__(self, current_gallery, *args, **kwargs):
        """
        Gallery form needs extending init because of title validation - it has to obtain current title in some way
        if gallery is edited.
        :param current_gallery:
        :param args: FlaskForm arguments
        :param kwargs: FlaskForm arguments
        """
        super(self.__class__, self).__init__(*args, **kwargs)  # get FlaskForm init arguments
        self.current_gallery = current_gallery

    title = StringField(label='Tytuł',
                        validators=[
                            DataRequired(message='Musisz podać tytuł.'),
                            Length(min=3, max=120, message='Podany tytuł powinien mieć od 3 do 120 znaków.')
                        ])
    thumbnail = FileField(label='Miniaturka',
                          validators=[
                              DataRequired(message='Musisz dodać miniaturkę.'),
                              FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                          ])
    images = FileField(label='Obrazy',
                       render_kw={'multiple': True},
                       validators=[
                           DataRequired(message='Musisz dodać obrazy.'),
                           FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku(ów) (.jpg, .png).')
                       ])
    submit = SubmitField(label='Zapisz')

    def validate_title(self, title):  # TODO test it
        secure_title = secure_filename(title.data)
        if secure_title != self.current_gallery:
            gallery = Galleries.\
                query.filter_by(secure_title=secure_title).first()

            if gallery:
                raise ValidationError('Ten tytuł jest zajęty. Wybierz inny.')
