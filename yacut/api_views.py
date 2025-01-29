from http import HTTPStatus

from flask import jsonify, request
from settings import Messages

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_full_short_url, get_unique_short_id
from .validators import is_valid_custom_id, is_valid_url


@app.route('/api/id/', methods=('POST',))
def create_id():
    data = request.get_json(silent=True)
    print(data)
    if data is None:
        raise InvalidAPIUsage(message=Messages.API_REQUIRED_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(message=Messages.API_REQUIRED_URL)
    if not is_valid_url(data['url']):
        raise InvalidAPIUsage(message=Messages.ORIG_URL_FORMAT)
    if (
        'custom_id' in data and
        not is_valid_custom_id(data['custom_id']) and
        data['custom_id'] not in (None, '')
    ):
        raise InvalidAPIUsage(message=Messages.API_BAD_CUSTOM_ID)
    if (
        'custom_id' in data and
        URLMap.query.filter_by(short=data['custom_id']).first() is not None
    ):
        raise InvalidAPIUsage(message=Messages.SHORT_URL_NOT_UNIQUE)
    if existing_url := URLMap.query.filter_by(short=data['url']).first():
        return jsonify(existing_url.to_dict()), HTTPStatus.CREATED
    if 'custom_id' not in data or data['custom_id'] in (None, ''):
        data['custom_id'] = get_unique_short_id()
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    response_data = url_map.to_dict()
    response_data['short_link'] = get_full_short_url(
        response_data['short_link']
    )
    return jsonify(response_data), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            Messages.API_SHORT_ID_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    print(url_map.original)
    return jsonify(url=url_map.original), HTTPStatus.OK
