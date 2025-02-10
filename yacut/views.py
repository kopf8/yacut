from http import HTTPStatus

from flask import abort, redirect, render_template

from . import app
from .forms import URLForm
from .utils import create_new_id, redirect_short


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    context = create_new_id({'original_link': form.original_link.data, 'custom_id': form.custom_id.data})
    form.original_link.data = context['original_link']
    form.custom_id.data = context['custom_id']
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=('GET',))
def redirect_to_original(short):
    url_map = redirect_short(short)
    if url_map is None:
        return abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
