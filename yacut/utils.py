from random import choice

from flask import url_for
from settings import Constants

from yacut.models import URLMap


def get_unique_short_id():
    while True:
        short_id = ''.join(
            (choice(Constants.SHORT_URL_CHARS)
             for _ in range(Constants.SHORT_URL_LEN))
        )
        db_match = URLMap.query.filter_by(short=short_id).first()
        if not db_match:
            return short_id


def get_full_short_url(short_id):
    print(url_for('redirect_to_original', short=short_id, _external=True))
    return url_for('redirect_to_original', short=short_id, _external=True)
