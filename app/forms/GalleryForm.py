import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Optional

from app.resources.GalleriesResource import Galleries


class GalleryForm(FlaskForm):
    def __init__(self, current_gallery, *args, **kwargs):
        """
        Gallery form needs extending init because of title validation - it has to obtain current title in some way
        if gallery is edited.
        :param current_gallery: gallery secure title:
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
    author = StringField(label='Autor',
                         validators=[
                             Optional(),
                             Length(max=120, message='Autor powinien mieć nie więcej niż 120 znaków.')
                         ])
    thumbnail = FileField(label='Miniaturka',
                          validators=[
                              FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                          ])
    images = FileField(label='Dodaj zdjęcia',
                       render_kw={'multiple': True},
                       validators=[
                           FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku(ów) (.jpg, .png).')
                       ])
    videos = StringField(label='Filmiki',
                         validators=[
                             Optional(),
                             Length(max=1024, message='Linki nie powinny zajmować więcej niż 1024 znaki.')
                         ],
                         render_kw={"placeholder": "linki do youtube oddzielone przecinkiem, "
                                                   "np: https://www.youtube.com/watch?v=dQw4w9WgXcQ, "
                                                   "https://www.youtube.com/watch?v=FTQbiNvZqaY"})
    submit = SubmitField(label='Zapisz')

    def validate_title(self, title):
        secure_title = secure_filename(title.data)
        if secure_title != self.current_gallery:
            gallery = Galleries. \
                query.filter_by(secure_title=secure_title).first()

            if gallery:
                raise ValidationError('Ten tytuł jest zajęty. Wybierz inny.')

    def validate_thumbnail(self, thumbnail):
        if not self.current_gallery and not thumbnail.data:
            raise ValidationError(message='Musisz dodać miniaturkę.')

    def validate_images(self, images):
        if not self.current_gallery and not images.data:
            raise ValidationError(message='Musisz dodać obrazy.')

    def validate_videos(self, videos):
        pattern = re.compile(
            '^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/('
                                        '?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(\?\S*)?$')

        for link in videos.data.split(','):
            link = link.strip()

            if not pattern.match(link):
                raise ValidationError('Niepoprawne linki Youtube.')
