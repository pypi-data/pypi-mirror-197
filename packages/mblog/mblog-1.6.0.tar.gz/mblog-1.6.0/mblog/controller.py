from __future__ import print_function

import os

from flask import flash, render_template, request, redirect, url_for
from peewee import IntegrityError
from werkzeug.utils import secure_filename

from mblog import database
from mblog.config import USER, UPLOAD_DIR


def deleteEntry(entry, template):
    try:
        with database.atomic():
            entry.delete_instance(recursive=True)
    except:
        flash('Error: Unable to delete entry.', 'danger')
    else:
        flash('Entry deleted successfully.', 'success')
    return render_template(template, entry=entry)


def createOrEditEntry(entry, template):
    if request.method == 'POST':
        entry.title = request.form.get('title') or ''
        entry.content = request.form.get('content') or ''
        entry.published = request.form.get('published') or False
        if not (entry.title and entry.content):
            flash('Title and Content are required.', 'danger')
        else:
            # Wrap the call to save in a transaction so we can roll it back
            # cleanly in the event of an integrity error.
            try:
                with database.atomic():
                    entry.save()
            except IntegrityError:
                flash('Error: this title is already in use.', 'danger')
            else:
                flash('Entry saved successfully.', 'success')
                if entry.published:
                    return redirect(url_for('detail', slug=entry.slug))
                return redirect(url_for('edit', slug=entry.slug))

    return render_template(template, entry=entry)


def uploadFile(template):
    if request.method == 'POST':
        try:
            file_uploaded = request.files.get('file')
            if not file_uploaded:
                flash('You did not upload a file. Please try again.', 'danger')
            else:
                filename = secure_filename(file_uploaded.filename)
                filepath = os.path.join(UPLOAD_DIR, filename)
                if not os.path.exists(UPLOAD_DIR):
                    os.makedirs(UPLOAD_DIR)
                file_uploaded.save(filepath)
                fileurl = url_for('files', filename=filename)
                flash(
                    'File saved successfully as'
                    ' <a href="{}">{}</a>.'.format(fileurl, filename), 'success')
        except:
            flash('Unable to save file. Please try again.', 'danger')

    return render_template(template)
