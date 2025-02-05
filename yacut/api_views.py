from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .utils import (create_new_id, short_link_exists)
from settings import Messages


@app.route('/api/id/', methods=('POST',))
def create_id():
    data = request.get_json(silent=True)
    return create_new_id(data)


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original(short_id):
    url_map = short_link_exists(short_id)
    if not url_map:
        raise InvalidAPIUsage(
            Messages.API_SHORT_ID_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    return jsonify(url=url_map.original), HTTPStatus.OK
