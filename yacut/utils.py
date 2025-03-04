from http import HTTPStatus
from random import choice

from flask import url_for, jsonify, flash, request

from yacut import db
from .exceptions import (BadCustomIdError, DuplicatedShortIdError,
                         IncorrectUrlFormatError, MissingBodyError,
                         MissingUrlError)
from .models import URLMap
from .validators import is_valid_custom_id, is_valid_url
from settings import Constants, Messages


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
    if orig_link_exists(data['url']):
        return jsonify(
            orig_link_exists(data['url']).to_dict()
        ), HTTPStatus.CREATED
    if 'custom_id' not in data or data['custom_id'] in (None, ''):
        data['custom_id'] = get_unique_short_id()


def save_data(obj):
    db.session.add(obj)
    db.session.commit()


def redirect_short(short):
    return short_link_exists(short)


def check_custom_id(data):
    if data:
        short = data
    else:
        short = get_unique_short_id()
    return short


def validate_process_form(context_data):

    if orig_link_exists(context_data['original_link']):
        url_map = orig_link_exists(context_data['original_link'])
        message = get_full_short_url(url_map.short)
        flash(message=message)
        return context_data

    if (
        context_data['custom_id'] and
        short_link_exists(context_data['custom_id'])
    ):
        message = Messages.SHORT_URL_NOT_UNIQUE
        flash(message=message)
        return

    short = check_custom_id(context_data['custom_id'])
    url_map = URLMap(
        original=context_data['original_link'],
        short=short
    )
    save_data(url_map)
    message = get_full_short_url(short)
    flash(message=message)
    context_data['original_link'] = context_data['custom_id'] = ''
    return context_data


def create_new_id(context_data):

    if context_data == request.get_json(silent=True):
        process_data(context_data)
        url_map = URLMap()
        url_map.from_dict(context_data)
        save_data(url_map)
        response_data = url_map.to_dict()
        return jsonify(response_data), HTTPStatus.CREATED

    return validate_process_form(context_data)
