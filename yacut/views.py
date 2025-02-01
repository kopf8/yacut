from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import (get_full_short_url, get_unique_short_id, orig_link_exists,
                    redirect_short, save_data, short_link_exists)
from settings import Messages


@app.route('/', methods=('GET', 'POST'))
def index_view():

    form = URLForm()

    if (
        form.validate_on_submit() and
        orig_link_exists(form.original_link.data)
    ):
        url_map = orig_link_exists(form.original_link.data)
        message = get_full_short_url(url_map.short)
        flash(message=message)
        return render_template('index.html', form=form)

    if (
        form.validate_on_submit() and
        form.custom_id.data and
        short_link_exists(form.custom_id.data)
    ):
        message = Messages.SHORT_URL_NOT_UNIQUE
        flash(message=message)
        return render_template('index.html', form=form)

    if form.validate_on_submit():
        if form.custom_id.data:
            short = form.custom_id.data
        else:
            short = get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short
        )
        save_data(url_map)
        message = get_full_short_url(short)
        flash(message=message)
        form.original_link.data = form.custom_id.data = ''
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=('GET',))
def redirect_to_original(short):
    url_map = redirect_short(short)
    if url_map is None:
        return abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
