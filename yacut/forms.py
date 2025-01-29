from flask_wtf import FlaskForm
from settings import Constants, Messages
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .validators import UniqueCustomId


class URLForm(FlaskForm):
    original_link = URLField(
        'Оригинальная длинная ссылка',
        validators=(
            DataRequired(message=Messages.REQUIRED_FIELD),
            Length(Constants.ORIG_URL_MIN_LEN,
                   Constants.ORIG_URL_MAX_LEN,
                   message=Messages.ORIG_URL_LEN),
            URL(message=Messages.ORIG_URL_FORMAT)
    ),
        description='Введите оригинальную длинную ссылку'
    )
    custom_id = StringField(
        'Короткая ссылка',
        validators=(
            Optional(),
            Length(Constants.SHORT_URL_MIN_LEN,
                   Constants.SHORT_URL_MAX_LEN,
                   message=Messages.SHORT_URL_LEN),
            Regexp(Constants.SHORT_URL_FORMAT,
                   message=Messages.SHORT_URL_FORMAT),
            UniqueCustomId()
        ),
        description=(f'Введите идентификатор из латинских букв и/или цифр '
                     f'длиной от {Constants.SHORT_URL_MIN_LEN} до '
                     f'{Constants.SHORT_URL_MAX_LEN} знаков, или '
                     f'оставьте поле пустым для генерации случайного '
                     f'набора знаков'),
    )
    create = SubmitField('Создать')
