from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .exceptions import (MissingBodyError, MissingUrlError,
                         IncorrectUrlFormatError, BadCustomIdError,
                         DuplicatedShortIdError)
from .models import URLMap
from .utils import (get_full_short_url, short_link_exists,
                    process_data, save_data)
from settings import Messages


@app.route('/api/id/', methods=('POST',))
def create_id():
    data = request.get_json(silent=True)
    try:
        process_data(data)
        url_map = URLMap()
        url_map.from_dict(data)
        save_data(url_map)
        response_data = url_map.to_dict()
        response_data['short_link'] = get_full_short_url(
            response_data['short_link']
        )
        return jsonify(response_data), HTTPStatus.CREATED

    except MissingBodyError:
        raise InvalidAPIUsage(message=Messages.API_REQUIRED_BODY)
    except MissingUrlError:
        raise InvalidAPIUsage(message=Messages.API_REQUIRED_URL)
    except IncorrectUrlFormatError:
        raise InvalidAPIUsage(message=Messages.ORIG_URL_FORMAT)
    except BadCustomIdError:
        raise InvalidAPIUsage(message=Messages.API_BAD_CUSTOM_ID)
    except DuplicatedShortIdError:
        raise InvalidAPIUsage(message=Messages.SHORT_URL_NOT_UNIQUE)


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original(short_id):
    url_map = short_link_exists(short_id)
    if not url_map:
        raise InvalidAPIUsage(
            Messages.API_SHORT_ID_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    return jsonify(url=url_map.original), HTTPStatus.OK
