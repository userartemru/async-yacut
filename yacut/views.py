from http import HTTPStatus

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.constants import DUPLICATED_SHORT_ID_MESSAGE
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, is_short_id_available
from yacut.yandex_disk import upload_files_to_yandex_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_link = None
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if not short_id:
            short_id = get_unique_short_id()
        elif not is_short_id_available(short_id):
            flash(DUPLICATED_SHORT_ID_MESSAGE)
            return render_template('index.html', form=form)

        url_map = URLMap(original=form.original_link.data, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        short_link = url_for(
            'redirect_view', short_id=url_map.short, _external=True
        )
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileUploadForm()
    uploaded_files = []
    if form.validate_on_submit():
        uploaded_files = await upload_files_to_yandex_disk(form.files.data)
        uploaded_files = save_file_links(uploaded_files)
    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


def save_file_links(files):
    uploaded_files = []
    for filename, download_link in files:
        short_id = get_unique_short_id()
        url_map = URLMap(original=download_link, short=short_id)
        db.session.add(url_map)
        uploaded_files.append({
            'filename': filename,
            'short_link': url_for(
                'redirect_view', short_id=short_id, _external=True
            ),
        })
    db.session.commit()
    return uploaded_files


@app.route('/<short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original, code=HTTPStatus.FOUND)
