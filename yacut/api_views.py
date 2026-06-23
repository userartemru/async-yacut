from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.constants import (
    DUPLICATED_SHORT_ID_MESSAGE,
    INVALID_SHORT_ID_MESSAGE,
)
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import (
    get_unique_short_id,
    is_short_id_available,
    is_valid_short_id,
)


@app.route('/api/id/', methods=['POST'], strict_slashes=False)
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    short_id = data.get('custom_id')
    if not short_id:
        short_id = get_unique_short_id()
    elif not is_valid_short_id(short_id):
        raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)
    elif not is_short_id_available(short_id):
        raise InvalidAPIUsage(DUPLICATED_SHORT_ID_MESSAGE)

    url_map = URLMap(original=data['url'], short=short_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view', short_id=url_map.short, _external=True
        ),
    }), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'], strict_slashes=False)
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
