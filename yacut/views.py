from http import HTTPStatus

from flask import abort, flash, redirect, render_template
from settings import Messages

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_full_short_url, get_unique_short_id


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = URLForm()
    if (
        form.validate_on_submit() and
        form.custom_id.data and
        URLMap.query.filter_by(short=form.custom_id.data).first()
    ):
        message = Messages.SHORT_URL_NOT_UNIQUE
        flash(message=message)
        return render_template('index.html', form=form)
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        message = get_full_short_url(short)
        flash(message=message)
        form.original_link.data = form.custom_id.data = ''
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=('GET',))
def redirect_to_original(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        return abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
