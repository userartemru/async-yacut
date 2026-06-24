from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, Regexp

from yacut.constants import (
    INVALID_SHORT_ID_MESSAGE,
    SHORT_IDENTIFIER_CHARACTERS,
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(SHORT_IDENTIFIER_CHARACTERS, message=INVALID_SHORT_ID_MESSAGE),
        ]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Загрузить')
