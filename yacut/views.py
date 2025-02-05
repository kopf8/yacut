from http import HTTPStatus

from flask import abort, redirect

from . import app
from .forms import URLForm
from .utils import redirect_short, create_new_id


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = URLForm()
    return create_new_id(form)


@app.route('/<string:short>', methods=('GET',))
def redirect_to_original(short):
    url_map = redirect_short(short)
    if url_map is None:
        return abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
