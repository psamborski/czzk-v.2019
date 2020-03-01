from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError


class MerchItemForm(FlaskForm):
    def __init__(self, current_item=None, *args, **kwargs):
        """
            Merch item form needs extending init because of photo validation - if it is edited, make photo not required.
            :param current_item: gallery secure title:
            :param args: FlaskForm arguments
            :param kwargs: FlaskForm arguments
            """
        super(self.__class__, self).__init__(*args, **kwargs)  # get FlaskForm init arguments
        self.current_item = current_item

    name = StringField(label='Nazwa',
                       validators=[
                           DataRequired(message='Musisz podać tytuł.'),
                           Length(min=3, max=120, message='Podana nazwa powinna mieć od 3 do 120 znaków.')
                       ])
    short_name = StringField(label='Krótka nazwa (do wyświetlenia w spisie)',
                             validators=[
                                 DataRequired(message='Musisz podać tytuł.'),
                                 Length(min=3, max=11, message='Skrócona nazwa powinna mieć od 3 do 11 znaków.')
                             ])
    price = IntegerField(label='Cena',
                         validators=[
                             Optional(),
                             NumberRange(min=0, message='Podana wartość nie jest liczbą')
                         ])
    description = StringField(label='Opis',
                              validators=[
                                  DataRequired(message='Musisz dodać opis.'),
                                  Length(min=3, max=1024, message='Podany opis musi mieć od 3 do 1024 znaków.')
                              ])
    photo = FileField(label='Zdjęcie (.jpg, .png)',
                      validators=[
                          FileAllowed(['jpg', 'png'], message='Nieprawidłowy format pliku (.jpg, .png).')
                      ])
    animation = FileField(label='Animacja (.gif - nieobowiązkowa)',
                          validators=[
                              Optional(),
                              FileAllowed(['gif'], message='Nieprawidłowy format pliku (.gif).')
                          ])
    submit = SubmitField(label='Zapisz')

    def validate_photo(self, photo):
        if not self.current_item and not photo.data:
            raise ValidationError('Musisz dodać zdjęcie.')
