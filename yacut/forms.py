from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from yacut.constants import (
    CUSTOM_SHORT_ID_MAX_LENGTH,
    INVALID_SHORT_ID_MESSAGE,
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=CUSTOM_SHORT_ID_MAX_LENGTH),
            Optional(),
            Regexp(r'^[A-Za-z0-9]+$', message=INVALID_SHORT_ID_MESSAGE),
        ]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Загрузить')
