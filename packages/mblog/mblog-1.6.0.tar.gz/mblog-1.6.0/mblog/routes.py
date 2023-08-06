from __future__ import print_function

import base64
import hashlib
import os
from datetime import datetime

from flask import request, session, flash, redirect, url_for, render_template, abort, send_file
from playhouse.flask_utils import object_list, get_object_or_404
from six.moves.urllib.parse import urlencode

from mblog import app
from mblog.config import USER, USERNAME, APP_README, UPLOAD_DIR
from mblog.controller import deleteEntry, createOrEditEntry, uploadFile
from mblog.models import Entry
from mblog.security import loginRequired


@app.route('/')
def index():
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())

    # The `object_list` helper will take a base query and then handle
    # paginating the results if there are more than 20. For more info see
    # the docs:
    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#object_list
    return object_list(
        'index.html',
        query,
        search=search_query,
        check_bounds=False,
        )


@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        # TODO: If using a one-way hash, you would also hash the
        # user-submitted password and do the comparison on the
        # hashed versions.
        hashed = base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()
        if hashed == app.config['ADMIN_PASSWORD_HASH']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html', next_url=next_url)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/create/', methods=['GET', 'POST'])
@loginRequired
def create():
    return createOrEditEntry(Entry(title='', content=''), 'create.html')


@app.route('/drafts/')
@loginRequired
def drafts():
    query = Entry.drafts().order_by(Entry.timestamp.desc())
    return object_list('index.html', query, check_bounds=False)


@app.route('/<slug>/')
def detail(slug):
    if session.get('logged_in'):
        query = Entry.select()
    else:
        query = Entry.public()
    if slug == 'README':
        entry = Entry(title='README', content=APP_README, slug=slug)
    else:
        entry = get_object_or_404(query, Entry.slug == slug)
    return render_template('detail.html', entry=entry)


@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@loginRequired
def edit(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    return createOrEditEntry(entry, 'edit.html')


@app.route('/<slug>/delete/', methods=['GET'])
@loginRequired
def delete(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    return deleteEntry(entry, 'delete.html')


@app.route('/upload/', methods=['GET', 'POST'])
@loginRequired
def upload():
    return uploadFile('upload.html')


@app.route('/files/<filename>')
def files(filename):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath)


@app.errorhandler(404)
def notFoundErrorHandler(exc):
    return render_template('notfound.html'), 404


@app.errorhandler(500)
def errorHandler(exc):
    return render_template('error.html'), 500


@app.template_filter('clean_querystring')
def cleanQueryString(request_args, *keys_to_remove, **new_values):
    # We'll use this template filter in the pagination include. This filter
    # will take the current URL and allow us to preserve the arguments in the
    # querystring while replacing any that we need to overwrite. For instance
    # if your URL is /?q=search+query&page=2 and we want to preserve the search
    # term but make a link to page 3, this filter will allow us to do that.
    querystring = dict((key, value)
                       for key, value in list(request_args.items()))
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urlencode(querystring)

@app.context_processor
def injectDefaults():
    return {'now': datetime.now(), 'user': USER, 'username': USERNAME}
