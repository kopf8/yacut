from http import HTTPStatus
from random import choice

from flask import url_for, jsonify

from . import db
from .exceptions import (MissingBodyError, MissingUrlError,
                         IncorrectUrlFormatError, BadCustomIdError,
                         DuplicatedShortIdError)
from .validators import is_valid_custom_id, is_valid_url
from settings import Constants
from yacut.models import URLMap


def short_link_exists(short_id):
    return URLMap.query.filter_by(short=short_id).first()


def orig_link_exists(url):
    return URLMap.query.filter_by(original=url).first()


def get_unique_short_id():
    while True:
        short_id = ''.join(
            (choice(Constants.SHORT_URL_CHARS)
             for _ in range(Constants.SHORT_URL_LEN))
        )
        if not short_link_exists(short_id):
            return short_id


def get_full_short_url(short_id):
    return url_for('redirect_to_original', short=short_id, _external=True)


def process_data(data):
    if data is None:
        raise MissingBodyError
    if 'url' not in data:
        raise MissingUrlError
    if not is_valid_url(data['url']):
        raise IncorrectUrlFormatError
    if (
        'custom_id' in data and
        not is_valid_custom_id(data['custom_id']) and
        data['custom_id'] not in (None, '')
    ):
        raise BadCustomIdError
    if (
        'custom_id' in data and
        short_link_exists(data['custom_id'])
    ):
        raise DuplicatedShortIdError
    if existing_url := short_link_exists(data['url']):
        return jsonify(existing_url.to_dict()), HTTPStatus.CREATED
    if 'custom_id' not in data or data['custom_id'] in (None, ''):
        data['custom_id'] = get_unique_short_id()


def save_data(obj):
    db.session.add(obj)
    db.session.commit()


def redirect_short(short):
    return short_link_exists(short)
