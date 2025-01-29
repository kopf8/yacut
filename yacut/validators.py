import re
from urllib.parse import urlparse

from settings import Constants, Messages
from wtforms.validators import ValidationError

from .models import URLMap


class UniqueCustomId:
    def __call__(self, form, field):
        db_match = URLMap.query.filter_by(short=field.data).first()
        if db_match:
            message = Messages.SHORT_URL_NOT_UNIQUE
            raise ValidationError(message=message)


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all((result.scheme, result.netloc))
    except ValueError:
        return False


def is_valid_custom_id(custom_id):
    return bool(re.match(Constants.SHORT_URL_FORMAT, custom_id))
